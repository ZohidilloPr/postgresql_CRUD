import psycopg2
from config.settings import config
from terminaltables import AsciiTable

# data deleting view

params = config()
conn = psycopg2.connect(**params) # connecting database
cursor = conn.cursor()

def DeleteSQLData(table):
    """ delete objects fields """
    id = (input("Enter object id: "))
    sql_show = f"SELECT * FROM {table} WHERE id = {id};"
    cursor.execute(sql_show) # prepeire sql query for postgresql
    db = cursor.fetchall()
    data = []
    data.append([col[0] for col in cursor.description]) # for table title
    for d in db:
        data.append(d)
    table__ = AsciiTable(data, title=f"Detail view") # make acsii table in terminal
    print("\n", table__.table, "\n")
    print("")
    if input("Are You sure ? (Y/n): ").lower() == "y":
        sql = f"DELETE FROM {table} WHERE id = {id};"
        cursor.execute(sql) # prepeire sql query for postgresql
        conn.commit() # push data to database
        print("deleting is successfully")
        if input("Delete again (y/n): ").lower() == "y":
            DeleteSQLData(table)

DeleteSQLData("subjects")