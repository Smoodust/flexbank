import sqlite3 as sl
import hashlib

def get_connection():
    return sl.connect(r'C:\Users\rusty\Desktop\Programming\Python projects\flexbank\database\database.db')

def check_authentication(conn, login, passw):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE login=? AND pass=?", (login, hashlib.sha256(passw.encode('utf-8')).hexdigest()))
    return len(cursor.fetchall()) > 0

def get_user_by_login_pass(conn, login, passw):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE login=? AND pass=?", (login, hashlib.sha256(passw.encode('utf-8')).hexdigest()))
    result = cursor.fetchall()[0]
    return {
        'id':result[0],
        'surname':result[1],
        'name':result[2],
        'patronymic':result[3],
        'phone':result[4],
        'date_of_birth':result[5]
    }

def get_accounts_by_user(conn, id_user):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE id_user=?", (id_user, ))
    result = cursor.fetchall()
    return [{
        'id':account[0],
        'type':account[2],
        'status':account[3],
        'number':account[4]
    } for account in result]

def get_active_accounts_by_user(conn, id_user):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE id_user=? AND status='active'", (id_user, ))
    result = cursor.fetchall()
    return [{
        'id':account[0],
        'type':account[2],
        'status':account[3],
        'number':account[4]
    } for account in result]

def get_cards_by_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CARDS WHERE id_account=?", (id_account, ))
    result = cursor.fetchall()
    return [{
        'id':card[0],
        'status':card[2],
        'card_numbe':card[3],
        'validity_period':card[4],
        'cvc':card[5]
    } for card in result]

def get_active_cards_by_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CARDS WHERE id_account=? AND status='active'", (id_account, ))
    result = cursor.fetchall()
    return [{
        'id':card[0],
        'status':card[2],
        'card_numbe':card[3],
        'validity_period':card[4],
        'cvc':card[5]
    } for card in result]

def block_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("UPDATE ACCOUNT SET status='blocked' WHERE id=? AND status='active'", (id_account, ))
    cursor.commit()

def activate_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("UPDATE ACCOUNT SET status='active' WHERE id=? AND status='blocked'", (id_account, ))
    cursor.commit()

def close_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("UPDATE ACCOUNT SET status='closed' WHERE id=? AND status='active'", (id_account, ))
    cursor.commit()

def block_card(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("UPDATE CARDS SET status='blocked' WHERE id=? AND status='active'", (id_card, ))
    cursor.commit()

def activate_card(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("UPDATE CARDS SET status='active' WHERE id=? AND status='blocked'", (id_card, ))
    cursor.commit()

def close_card(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("UPDATE CARDST SET status='closed' WHERE id=? AND status='active'", (id_card, ))
    cursor.commit()

def make_transaction():
    cursor = conn.cursor()
    cursor.execute("UINSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');", (id_card, ))
    cursor.commit()

def transfer_from_to_card(conn, from_card, to_card, amount):
    

login = 'WQLXCYMEUZ'
passw = 'BGdcN1G72e'

conn = get_connection()
cursor = conn.cursor()
#hashlib.sha256(x.encode('utf-8')).hexdigest()
if check_authentication(conn, login, passw):
    user = get_user_by_login_pass(conn, login, passw)
    print(get_cards_by_account(conn, 1))
conn.close()