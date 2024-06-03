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
        print(data_base_path)
    else:
        if len(sys.argv) == 3:
            data_base_path = sys.argv[2]

        file_path = sys.argv[1]
        print(file_path)

    raw_data: dict = converter.xml_to_dict_convert(file_path)

    sql_connection = sqlite3.connect(data_base_path)
    sql_cursor = sql_connection.cursor()

    db_inserter.initialize_data_base(sql_cursor)

    sql_connection.commit()
    sql_connection.close()
