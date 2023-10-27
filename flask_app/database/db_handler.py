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

def db_add_property(location, size_m, rooms, furniture, building_year):
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

            # Execute an SQL query to insert the data into the 'propertys' table
        insert_query = "INSERT INTO propertys (location, size_m, rooms, furniture, building_year) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(insert_query, (location, size_m, rooms, furniture, building_year))

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()




