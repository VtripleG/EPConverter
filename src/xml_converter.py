import xmltodict


def xml_to_dict_convert(file_name: str) -> dict:
    with (open(file_name, 'r', encoding='utf16') as xml_file):
        xml_data = xmltodict.parse(xml_file.read())
    return xml_data


def get_discipline_list(raw_data: dict) -> dict:
    d_list: dict = {}

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ПланыСтроки']:
        d_list[object['@Код']] = object['@Дисциплина'] + ':' + object['@КодКафедры']

    return d_list
   

def get_educational_program_inf(raw_data: dict) -> dict:
    ed_inf: dict = {}

    ed_inf['profile'] = raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ООП']['ООП']['@Название']
    ed_inf['name'] = raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ООП']['@Название']
    ed_inf['code'] = raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ООП']['@Шифр']
    ed_inf['start_year'] = raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['Планы']['@ГодНачалаПодготовки']
    ed_inf['form'] = int(raw_data['Документ']['@КодФормыОбучения'])

    if ed_inf['form'] == 1:
        ed_inf['form'] = 'Очная'
    elif ed_inf['form'] == 2:
        ed_inf['form'] = 'Заочная'
    else:
        ed_inf['form'] = 'Очно-заочная'

    return ed_inf


def get_full_inf(raw_data: dict) -> dict:
    pass