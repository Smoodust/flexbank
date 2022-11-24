import sqlite3 as sl
import hashlib


def get_connection():
    return sl.connect('C:/Users/USER/Documents/flexbank/database/database.db')

def is_users_login_pass_good(conn, login, passw):
    cursor = conn.cursor()
    pass_hash = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    return len(cursor.execute('SELECT login, pass from USER WHERE login=? AND pass=?', (login, pass_hash))) > 0

def get_user_by_login_pass(conn, login, passw):
    cursor = conn.cursor()
    pass_hash = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    cursor.execute('SELECT id, surname, name, patronymic, phone, date_of_birth from USER WHERE login=? AND pass=?', (login, pass_hash))
    try:
        return cursor.fetchall()
    except sqlite3.DatabaseError as err:       
        print("Error: ", err)

conn = get_connection()
print(get_user_by_login_pass(conn, input('Login: '), input('Passw: ')))
conn.close()