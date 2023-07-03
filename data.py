
# tablelar qo'shish

subject_table = """
    CREATE TABLE IF NOT EXISTS subjects (
        id BIGSERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (80) NOT NULL UNIQUE,
        add_time DATE DEFAULT CURRENT_DATE
    );
"""

teacher_table = """
    CREATE TABLE IF NOT EXISTS teachers (
        id BIGSERIAL NOT NULL PRIMARY KEY,
        f_name VARCHAR (80) NOT NULL,
        l_name VARCHAR (80) NOT NULL,
        phone VARCHAR(13) UNIQUE,
        subject BIGINT REFERENCES subjects(id),
        add_time DATE DEFAULT CURRENT_DATE
    );
"""

student_table = """
    CREATE TABLE IF NOT EXISTS students (
        id BIGSERIAL NOT NULL PRIMARY KEY,
        f_name VARCHAR (80) NOT NULL,
        l_name VARCHAR (80) NOT NULL,
        phone VARCHAR(13) UNIQUE,
        teacher BIGINT REFERENCES teachers(id),
        subject BIGINT REFERENCES subjects(id),
        add_time DATE DEFAULT CURRENT_DATE
    );
"""

def creates_tables(cursor, conn):
    """ databasega tablelarni qo'shish uchun """
    
    cursor.execute(subject_table)
    cursor.execute(teacher_table)
    cursor.execute(student_table)

    # databaseni yopish uchun
    conn.commit()


