import psycopg2
from .read import MakeTableSqlQuery
from config.settings import config

# data adding views

params = config()
conn = psycopg2.connect(**params) # connecting database
cursor = conn.cursor()

def WriteData(cursor, conn):
    """ main function for write data to postgresql """
    survey_add = input("Do you want to add data which table: \n\nIf you add first time to database: 1.Subject 2. Teacher next Students add \n\
    \n\t1. Teachers\n\t2. Students\n\t3. Subjects\n\n: ")
    if survey_add == "1": sql = AddTeacher()
    elif survey_add == "2": sql = AddStudent()
    elif survey_add == "3": sql = AddSubject()
    cursor.execute(sql) # prepeire sql query for postgresql
    conn.commit() # push data to database
    print("Saving is successfully")
    again = input("Do you want add data again ? (Y/n): ").lower()
    if again == "y":
        WriteData(cursor, conn)


def AddSubject():
    """ SUBJECTS add to PostgreSQL """
    name = input("Subject Name: ")
    insert_data = "INSERT INTO subjects (name) VALUES ('{}');".format(name)
    return insert_data


def AddTeacher():
    """ Teachers Add to Database """
    f_name = input("First Name: ")
    l_name = input("Last Name: ")
    phone = input("Phone Number: ")
    print("If You don't find you choice, You can update items.")    
    MakeTableSqlQuery(cursor, ["id", "name"], sql="SELECT id, name,  FROM subjects;", title_table="Subjects List")
    subject = input("Subject ID: ")
    insert_data = "INSERT INTO teachers (f_name, l_name, phone, subject) VALUES ('{}', '{}', '{}', '{}');".format(f_name, l_name, phone, subject)
    return insert_data


def AddStudent():
    """ Students Add To Database """
    f_name = input("First Name: ")
    l_name = input("Last Name: ")
    phone = input("Phone Number: ")
    print("If You don't find you choice, You can update items.")
    MakeTableSqlQuery(cursor, ["id", "f_name", "teacher_subject"], sql="SELECT teachers.id, teachers.f_name, subjects.name FROM teachers JOIN subjects ON teachers.subject = subjects.id;", title_table="Teachers List")
    teacher = input("Teacher ID: ")
    MakeTableSqlQuery(cursor, ["id", "name"], sql="SELECT id, name FROM subjects;", title_table="Subjects List")
    subject = input("Subject ID: ")
    insert_data = "INSERT INTO students (f_name, l_name, phone, teacher, subject) VALUES ('{}', '{}', '{}', '{}', '{}');".format(f_name, l_name, phone, teacher, subject)
    return insert_data

