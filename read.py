from update import UpdateSQLData
from terminaltables import AsciiTable # table in terminal
# data reading views.

def ReadData(cursor):
    """ cycle for read data """
    survey_read = input("Do you want see which table: \
    \n\t1. Teachers\n\t2. Students\n\t3. Subjects\n\t4. Exit\n\n: ")
    print()
    if survey_read == "1": 
        sql = GetALLData(which_data="teachers")
        MakeTableSqlQuery(cursor, ["id", "first Name", "last Name", "subject", "register_time"], sql, title_table="Teachers List")
        ExtraOpportunities(table="teachers", cursor=cursor)
    elif survey_read == "2": 
        sql = GetALLData(which_data="students")
        MakeTableSqlQuery(cursor, ["id", "first name", "last name", "teacher", "subject", "register_time"], sql, title_table="Students List")
        ExtraOpportunities(table="students", cursor=cursor)
    elif survey_read == "3": 
        sql = GetALLData(which_data="subjects")
        MakeTableSqlQuery(cursor, ["id", "name", "add_time"], sql, title_table="Subjects List")
        ExtraOpportunities(table="subjects", cursor=cursor)
    else:
        pass
    print("\n")
    again = input("Do You want see data again ? (Y/n): ").lower()
    if again == "y":
        ReadData(cursor)

def GetALLData(which_data):
    """ 
        sql = GetALLData(which_data=`table_name`) --> 
        --> return command all data show in given table. 
    """
    tables = ["students", "teachers", "subjects"] # exist tables
    if which_data in tables: # check arguments
        if which_data == "teachers":
            # teacher data
            command = f"""
                SELECT {which_data}.id, {which_data}.f_name, {which_data}.l_name, subjects.name, {which_data}.add_time AS register_time FROM {which_data} LEFT JOIN subjects ON teachers.subject = subjects.id ORDER BY {which_data}.id;
            """
            return command
        elif which_data == "students":
            # student data
            command = f"""
                SELECT {which_data}.id, {which_data}.f_name, {which_data}.l_name, teachers.f_name, subjects.name, {which_data}.add_time AS register_time FROM {which_data} LEFT JOIN subjects ON students.subject = subjects.id LEFT JOIN teachers ON students.teacher = teachers.id ORDER BY {which_data}.id;
            """
            return command
        else:
            # subject data
            command = f"""
                SELECT * FROM {which_data} ORDER BY {which_data}.id;
            """
            return command
    else:
        print("Bunday table nomi topilmadi")
        return False


def MakeTableSqlQuery(cursor, table_names, sql, title_table):
    """
        MakeTableSqlQuery(cursor, list: table_names=["id", "some tables names", vhk], sql=sql_query, title=str(title table if you want))
        make acsii table taken sql query data 
    """
    cursor.execute(sql) # make sql query for postgresql
    db = cursor.fetchall()
    data = []
    data.append(table_names) # for table title
    for d in db:
        data.append(d)
    table = AsciiTable(data, title=f"{title_table}") # make acsii table in terminal
    print(table.table)
    print()


def ExtraOpportunities(table, cursor):
    """ 
        extra opportunities for detail of data, extra queries
    """
    extra = input("extra opportuinites (if you want to use): \n\n\t1. Search\n\t2. Detail\n\t3. Update\n\nYour Option: ")
    if extra == "3":
        UpdateSQLData(table)
    if table == "teachers": 
        table_names = ["id", "f_name", "last_name", "subject", "register_time"]
        if extra == "1":
            words = input("Enter Any words: ")
            sql=f"SELECT teachers.id, teachers.f_name, teachers.l_name, subjects.name, teachers.add_time FROM teachers JOIN subjects ON teachers.subject = subjects.id WHERE teachers.f_name ILIKE '%{words}%' OR teachers.l_name ILIKE '%{words}%' OR subjects.name ILIKE '%{words}%' ORDER BY teachers.id;"
            MakeTableSqlQuery(cursor=cursor, table_names=table_names, sql=sql, title_table="Searching results")
            ExtraOpportunities(table, cursor)
        elif extra == "2":
            DetailSQLQuery(table, cursor)
    elif table == "students": 
        table_names = ["id", "f_name", "last_name", "teacher", "subject", "register_time"]
        if extra == "1":
            words = input("Enter Any words: ")
            sql=f"SELECT students.id, students.f_name, students.l_name, teachers.f_name, subjects.name, students.add_time FROM students JOIN subjects ON students.subject = subjects.id JOIN teachers ON students.teacher = teachers.id WHERE students.f_name ILIKE '%{words}%' OR students.l_name ILIKE '%{words}%' OR subjects.name ILIKE '%{words}%' OR teachers.f_name = '{words}' ORDER BY students.id;"
            MakeTableSqlQuery(cursor=cursor, table_names=table_names, sql=sql, title_table="Searching results")
            ExtraOpportunities(table, cursor)
        elif extra == "2":
            DetailSQLQuery(table, cursor)
    elif table == "subjects": 
        table_names = ["id", "name", "register_time"]
        if extra == "1":
            words = input("Enter Any words: ")
            sql=f"SELECT * FROM subjects WHERE name ILIKE '%{words}%' ORDER BY id;"
            MakeTableSqlQuery(cursor=cursor, table_names=table_names, sql=sql, title_table="Searching results")        
            ExtraOpportunities(table, cursor)
        elif extra == "2":
            DetailSQLQuery(table, cursor)


def DetailSQLQuery(table, cursor):
    """
        detail of taken data
    """
    try:
        get_id = int(input("Enter object ID: "))
        print()
        if table == "teachers":
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "First Name", "Last Name", "Phone Number", "Register Time"], sql=f"SELECT id, f_name, l_name, phone, add_time FROM teachers WHERE id = {get_id};", title_table="Teacher's detail data")
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "Teaching Subjects Name"], sql=f"SELECT subjects.id, subjects.name FROM teachers JOIN subjects ON teachers.subject = subjects.id WHERE teachers.id = {get_id}", title_table="")
        elif table == "students":
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "First Name", "Last Name", "Phone Number", "Register Time"], sql=f"SELECT id, f_name, l_name, phone, add_time FROM students WHERE id = {get_id};", title_table="Student's detail data")
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "First Name", "Last Name", "Phone Number", "Teaching Subject"], sql=f"SELECT teachers.id, teachers.f_name, teachers.l_name, teachers.phone, subjects.name FROM students JOIN teachers ON students.teacher = teachers.id JOIN subjects ON teachers.subject = subjects.id WHERE students.id = {get_id};", title_table="Teacher's detail data")
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "Learning Subjects Name"], sql=f"SELECT subjects.id, subjects.name FROM students JOIN subjects ON students.subject = subjects.id WHERE students.id = {get_id}", title_table="Learning Subjects data")
        elif table == "subjects":
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "Name", "Register Time"], sql=f"SELECT * FROM subjects WHERE id = {get_id};", title_table="Subject's detail data")
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "First Name", "Last Name", "Phone Number", "Subject Name"], sql=f"SELECT teachers.id, teachers.f_name, teachers.l_name, teachers.phone, subjects.name FROM subjects JOIN teachers ON teachers.subject = subjects.id WHERE subjects.id = {get_id};", title_table="Teachers")
            MakeTableSqlQuery(cursor=cursor, table_names=["id", "First Name", "Last Name", "Phone Number", "Teacher First Name", "Subject Name"], sql=f"SELECT students.id, students.f_name, students.l_name, students.phone, teachers.f_name, subjects.name FROM subjects JOIN students ON students.subject = subjects.id JOIN teachers ON teachers.subject = subjects.id WHERE subjects.id = {get_id};", title_table="Students")
    except Exception as e:
        pass