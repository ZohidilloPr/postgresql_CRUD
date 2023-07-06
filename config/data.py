
# tablelar qo'shish

users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL NOT NULL PRIMARY KEY,
        f_name VARCHAR (80),
        l_name VARCHAR (80),
        is_active BOOLEAN DEFAULT TRUE,
        staff BOOLEAN DEFAULT FALSE,
        superuser BOOLEAN DEFAULT FALSE, 
        username VARCHAR (100) NOT NULL UNIQUE,
        password VARCHAR (200) NOT NULL,
        joined_date DATE DEFAULT CURRENT_DATE,
        last_login TIMESTAMP
    );
"""

default_user = """
    INSERT INTO users (username, password, staff, superuser)
    SELECT '@guest', 'guest', 'TRUE', 'FALSE'
    WHERE NOT EXISTS (SELECT * FROM users WHERE username = '@guest');
"""

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
    
    cursor.execute(users_table)
    cursor.execute(default_user)
    cursor.execute(subject_table)
    cursor.execute(teacher_table)
    cursor.execute(student_table)

    # databaseni yopish uchun
    conn.commit()


