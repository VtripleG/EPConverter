import sqlite3


def initialize_data_base(cursor : sqlite3.Cursor):
    with open('./data/template.sql', 'r') as file:
        ini_sql_querys = file.read()

    for query in ini_sql_querys.split(';'):
        cursor.execute(query)


def insert_disciplines(discipline_list: dict, educational_program_direction_code: str, cursor: sqlite3.Cursor):
    for key in discipline_list.keys():
        cursor.execute(f"INSERT INTO disciplines(code, educational_program_id, name, department_code) VALUES({key}, "
                       f"(SELECT id from educational_programs WHERE direction_code = "
                       f"{educational_program_direction_code}), {discipline_list[key].split(':')[0]}, "
                       f"{discipline_list[key].split(':')[1]})")




def insert_competencies_guide(competence_guide: dict, educational_program_direction_code: str, cursor: sqlite3.Cursor):
    pass
    # INSERT INTO competencies_guide(competence_code, educational_program_id, content) VALUES(10, (SELECT id from educational_programs WHERE direction_code = 8), 'aaaaaa')


def insert_competencies_list(competence_list: dict, cursor: sqlite3.Cursor):
    pass


def insert_educational_program(program_list: dict, cursor: sqlite3.Cursor):
    cursor.execute(f"INSERT INTO educational_programs(direction_code, direction_name, profile, start_year, education_form) "
                   f"VALUES({program_list['code']}, {program_list['name']}, {program_list['profile']}, "
                   f"{program_list['start_year']}, {program_list['form']})")


def insert_laboriousness(laboriousness_list: dict, cursor: sqlite3.Cursor):
    pass

