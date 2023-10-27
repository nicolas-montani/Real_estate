import sqlite3
from sqlite3 import Error

DATABASE = r"flask_app/database/database.sql"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print("Connection Error :" + str(e))

    return conn

def add(db_file, table, values):
    conn = create_connection(db_file)
    c = conn.cursor()
    c.execute("INSERT INTO " + table + " VALUES (" + values + ")")
    conn.commit()
    conn.close()

def get(db_file, table, id):
    conn = create_connection(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM " + table + " WHERE id = " + str(id))
    return c.fetchall()

def search(db_file, table, keyword):
    conn = create_connection(db_file)
    c = conn.cursor()
    # Use the SQL LIKE clause to search for the keyword in the specified table
    c.execute("SELECT * FROM " + table + " WHERE column_name LIKE ?",
              ('%' + keyword + '%',))
    return c.fetchall()



