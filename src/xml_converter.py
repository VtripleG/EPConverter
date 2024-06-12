import xmltodict


def xml_to_dict_convert(file_name: str) -> dict:
    with (open(file_name, 'r', encoding='utf16') as xml_file):
        xml_data = xmltodict.parse(xml_file.read())
    return xml_data


def get_discipline_list(raw_data: dict) -> list:
    d_list: list = []

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ПланыСтроки']:
        buffer: dict = {}
        buffer['Код'] = object['@Код']
        buffer['Название'] = object['@Дисциплина']

        if '@КодКафедры' in object.keys(): 
            buffer['Код кафедры'] = object['@КодКафедры'] 
        else:
            buffer['Код кафедры'] = '0'

        d_list.append(buffer)

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

    return ed_inf


def get_laboriousness_ochnoe(raw_data: dict) -> list:
    hours_type_guide: dict = {}

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['СправочникВидыРабот']:
        hours_type_guide[object['@Код']] = object['@Название']

    laboriousness: list = []
    
    # print(hours_type_guide)

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ПланыНовыеЧасы']:
        buffer: dict = {}

        if (object['@КодТипаЧасов'] == '3' or object['@КодТипаЧасов'] == '5'):
            continue

        buffer['Код дисциплины'] = object['@КодОбъекта']
        buffer['Номер семестра'] = str(int(object['@Курс']) * 2 - 1 + int(object['@Семестр']) - 1)
        buffer['Вид работы'] = hours_type_guide[object['@КодВидаРаботы']]
        buffer['Количество часов'] = object['@Количество']
        laboriousness.append(buffer)

    return laboriousness


def get_laboriousness_zaochnoe(raw_data: dict) -> list:
    hours_type_guide: dict = {}

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['СправочникВидыРабот']:
            hours_type_guide[object['@Код']] = object['@Название']
    
    laboriousness: list = []

    # print(hours_type_guide)

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ПланыНовыеЧасы']:
        buffer: dict = {}

        if (object['@КодТипаЧасов'] == '3' or object['@КодТипаЧасов'] == '5' or object['@Семестр'] != '0') :
            continue

        buffer['Код дисциплины'] = object['@КодОбъекта']
        buffer['Номер семестра'] = str(int(object['@Курс']) * 2 - 1 + ((int(object['@Сессия']) - 1) // 2))
        buffer['Вид работы'] = hours_type_guide[object['@КодВидаРаботы']]
        buffer['Количество часов'] = object['@Количество']
        laboriousness.append(buffer)

    return laboriousness


def get_competence_guide(raw_data: dict) -> list:
    comp_list: list = []

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ПланыКомпетенции']:
        buffer: dict = {}

        buffer['Шифр'] = object['@ШифрКомпетенции']
        buffer['Код'] = object["@Код"]
        buffer['Название'] = object['@Наименование']
        comp_list.append(buffer)

    return comp_list


def get_competence_list(raw_data: dict) -> list:
    comp_list: list = []

    for object in raw_data['Документ']['diffgr:diffgram']['dsMMISDB']['ПланыКомпетенцииДисциплины']:
        buffer: dict = {}
        buffer['Код дисциплины'] = object['@КодСтроки']
        buffer['Код компетенции'] = object['@КодКомпетенции']
        comp_list.append(buffer)

    return comp_list
