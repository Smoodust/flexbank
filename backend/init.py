import sqlite3 as sl

def get_connection():
    return sl.connect('C:/Users/USER/Documents/flexbank/database/database.db')

conn = get_connection()
cursor = conn.cursor()
conn.close()