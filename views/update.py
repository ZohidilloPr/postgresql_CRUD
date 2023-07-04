import psycopg2
from config.settings import config

# data updateting view

params = config()
conn = psycopg2.connect(**params) # connecting database
cursor = conn.cursor()

def UpdateSQLData(table):
    """ update objects fields """
    id = (input("Enter object id: "))
    cursor.execute(f"SELECT * FROM {table} WHERE id = {id};")
    print("Exists Fields Name: \n", [fields[0] for fields in cursor.description])
    field = input("Field name: ")
    value = input("Value: ")
    sql = f"UPDATE {table} SET {field} = '{value}' WHERE id = {id};"
    cursor.execute(sql) # prepeire sql query for postgresql
    if input("Are You sure ? (Y/n): ").lower() == "y":
        conn.commit() # push data to database
        print("updating is successfully")
        if input("Update again (y/n): ").lower() == "y":
            UpdateSQLData(table)