import sqlite3


def initialize_data_base(cursor: sqlite3.Cursor):
    with open('../data/template.sql', 'r') as file:
        ini_sql_queries = file.read()

    for query in ini_sql_queries.split(';'):
        cursor.execute(query)


def insert_disciplines(discipline_list: list,
                       educational_program_id: str,
                       cursor: sqlite3.Cursor):
    for object in discipline_list:
        try:
            cursor.execute("""
                    INSERT INTO disciplines(code, educational_program_id, name, department_code) 
                    VALUES(?, ?, ?, ?)""", 
                    (object['Код'], educational_program_id, 
                     object['Название'], object['Код кафедры']))
        except sqlite3.IntegrityError as e:
            print(f"Невозможно вставить в БД {object['Название']}: {object['Код']}")


def insert_competencies_guide(competence_guide: list,
                              educational_program_id: str,
                              cursor: sqlite3.Cursor):
    try:
        for object in competence_guide:
            cursor.execute("""
                INSERT INTO competencies_guide(competence_code, educational_program_id, content, code) 
                VALUES(?, ?, ?, ?)""",
                (object['Шифр'], educational_program_id, 
                 object['Название'], object['Код']))
    except sqlite3.IntegrityError as e:
        print(f"Невозможно вставить в БД {object['Шифр']}: {object['Название']}")


def insert_competencies_list(competence_list: list,
                             educational_program_id: str,
                             cursor: sqlite3.Cursor):
    for object in competence_list:
        try:
            cursor.execute(f"""
        INSERT INTO competencies_list(discipline_id, competence_guide_id) 
        VALUES(
        (SELECT disciplines.id FROM disciplines WHERE disciplines.code = ? AND disciplines.educational_program_id = ?),
        (SELECT competencies_guide.id FROM competencies_guide WHERE competencies_guide.code = ? AND competencies_guide.educational_program_id = ?)
        )""",
        (object['Код дисциплины'], educational_program_id, 
         object['Код компетенции'], educational_program_id)
        )
        except sqlite3.IntegrityError as e:
            print(f"Ошибка при вставке: {str(e)}")


def insert_educational_program(program_list: dict, cursor: sqlite3.Cursor) -> str:
    try:
        cursor.execute("""
                INSERT INTO educational_programs(direction_code, direction_name, profile, start_year, education_form) 
                VALUES(?, ?, ?, ?, ?)
            """, (program_list['code'], program_list['name'], program_list['profile'], int(program_list['start_year']),
                program_list['form']))
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при вставке: {str(e)}")

    cursor.execute("""
    SELECT educational_programs.id FROM educational_programs 
    WHERE educational_programs.direction_code = ? AND educational_programs.education_form = ?
    """, (program_list['code'], program_list['form']))    

    result: str = cursor.fetchone()[0]

    return result


def insert_laboriousness(laboriousness_list: list,
                          educational_program_id: str, 
                          cursor: sqlite3.Cursor):
    for object in laboriousness_list:
        try:
            cursor.execute(f"""
            INSERT INTO laboriousness(descipline_id, semester_number, work_type, hours_number)
            VALUES( 
                (SELECT disciplines.id FROM disciplines 
                WHERE disciplines.code = ? AND 
                disciplines.educational_program_id = ?),?, ?, ?)""",
            (object['Код дисциплины'], educational_program_id, 
             object['Номер семестра'], object['Вид работы'], 
             object['Количество часов'])
        )
        except sqlite3.IntegrityError as e:
            print(object)
            print(f"Ошибка при вставке: {str(e)}")
