import sqlite3
import sys
import xml_converter as converter
import data_base_inserter as db_inserter


if __name__ == '__main__':
    data_base_path: str = './DB.db'
    file_path: str = ''
    if len(sys.argv) <= 1:
        print('Enter path to *.plx file')
        file_path = input()
        print(file_path)
    
        print('Enter path to data base')
        data_base_path = input()
    else:
        if len(sys.argv) == 3:
            data_base_path = sys.argv[2]
    
        file_path = sys.argv[1]

    raw_data: dict = converter.xml_to_dict_convert(file_path)

    sql_connection = sqlite3.connect(data_base_path)
    sql_cursor = sql_connection.cursor()

    db_inserter.initialize_data_base(sql_cursor)

    ed_program_inf: dict = converter.get_educational_program_inf(raw_data)
    discipline_list: list = converter.get_discipline_list(raw_data)
    competence_guide_list: list = converter.get_competence_guide(raw_data)
    competence_list: list = converter.get_competence_list(raw_data)
    laboriousness_list: list = converter.get_laboriousness_ochnoe(raw_data)
    # laboriousness_list: list = converter.get_laboriousness_zaochnoe(raw_data)

    ed_id: str = db_inserter.insert_educational_program(ed_program_inf, sql_cursor)
    sql_connection.commit()

    db_inserter.insert_disciplines(discipline_list, ed_id, sql_cursor)
    sql_connection.commit()

    db_inserter.insert_competencies_guide(competence_guide_list, ed_id, sql_cursor)
    sql_connection.commit()

    db_inserter.insert_competencies_list(competence_list, ed_id, sql_cursor)
    sql_connection.commit()

    db_inserter.insert_laboriousness(laboriousness_list, ed_id, sql_cursor)
    sql_connection.commit()

    sql_connection.close()
