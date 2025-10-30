# SQLite Helper Functions

import sqlite3


def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
    except Error as e:
        print(e)
    return conn


def close_connection(conn):
    """ Close the database connection """
    if conn:
        conn.close()
        print("Connection closed")


def execute_query(conn, query):
    """ Execute a single query """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        print("Query executed successfully")
    except Error as e:
        print(f"Error: {e}")
