import sqlite3 as sl
import hashlib
import datetime

def get_connection():
    return sl.connect(r'C:\Users\USER\Documents\flexbank\database\database.db', check_same_thread=False)

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
        'id_user':account[1],
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
        'id_user':account[1],
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
        'id_account':card[1],
        'status':card[2],
        'card_number':card[3],
        'validity_period':card[4],
        'cvc':card[5]
    } for card in result]

def get_active_cards_by_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CARDS WHERE id_account=? AND status='active'", (id_account, ))
    result = cursor.fetchall()
    return [{
        'id':card[0],
        'id_account':card[1],
        'status':card[2],
        'card_number':card[3],
        'validity_period':card[4],
        'cvc':card[5]
    } for card in result]

def get_account_by_id(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ACCOUNT WHERE id=?", (id_account, ))
    account = cursor.fetchall()[0]
    return {
        'id':account[0],
        'id_user':account[1],
        'type':account[2],
        'status':account[3],
        'number':account[4]
    }

def get_card_by_id(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CARDS WHERE id=?", (id_card, ))
    card = cursor.fetchall()[0]
    return {
        'id':card[0],
        'id_account':card[1],
        'status':card[2],
        'card_number':card[3],
        'validity_period':card[4],
        'cvc':card[5]
    }

def block_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("UPDATE ACCOUNT SET status='blocked' WHERE id=? AND status='active'", (id_account, ))
    conn.commit()

def activate_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("UPDATE ACCOUNT SET status='active' WHERE id=? AND status='blocked'", (id_account, ))
    conn.commit()

def close_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("UPDATE ACCOUNT SET status='closed' WHERE id=? AND status='active'", (id_account, ))
    conn.commit()

def block_card(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("UPDATE CARDS SET status='blocked' WHERE id=? AND status='active'", (id_card, ))
    conn.commit()

def activate_card(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("UPDATE CARDS SET status='active' WHERE id=? AND status='blocked'", (id_card, ))
    conn.commit()

def close_card(conn, id_card):
    cursor = conn.cursor()
    cursor.execute("UPDATE CARDS SET status='closed' WHERE id=? AND status='active'", (id_card, ))
    conn.commit()

def get_transactions_by_user(conn, id_user):
    accounts = get_accounts_by_user(conn, id_user)
    accounts_id = ['id_account='+str(x['id']) for x in accounts]
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TRANSACTIONS WHERE "+' OR '.join(accounts_id))
    result = cursor.fetchall()
    return [{
        'id':news[0],
        'id_account':news[1],
        'type':news[2],
        'date':news[3],
        'amount':news[4],
        'another_subject':news[5]
    } for news in result] 

def get_sum_transaction_user(conn, id_user):
    transactions = get_transactions_by_user(conn, id_user)
    return sum([abs(x['amount']) if x['amount'] < 0 else 0 for x in transactions])

def get_diff_transaction_account(conn, id_account):
    transactions = get_transactions_by_account(conn, id_account)
    return sum([x['amount'] for x in transactions])

def get_diff_transaction_user(conn, id_user):
    transactions = get_transactions_by_user(conn, id_user)
    return sum([x['amount'] for x in transactions])

def get_transactions_by_account(conn, id_account):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TRANSACTIONS WHERE id_account=?", (id_account, ))
    result = cursor.fetchall()
    return [{
        'id':news[0],
        'id_account':news[1],
        'type':news[2],
        'date':news[3],
        'amount':news[4],
        'another_subject':news[5]
    } for news in result] 

def make_transaction(conn, id_account, type, date, amount, another_subject):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customers (id_account, type, date, amount, another_subject) VALUES (?, ?, ?, ?, ?);", (id_account, type, date, amount, another_subject))
    cursor.commit()

def make_between_our_cards(conn, id_from, id_to, amount):
    card_from = get_card_by_id(conn, id_from)
    card_to = get_card_by_id(conn, id_to)
    make_transaction(conn, card_from['id_account'], card_to['id_account'], datetime.today().strftime("%d/%m/%y"), -amount)
    make_transaction(conn, card_to['id_account'], card_from['id_account'], datetime.today().strftime("%d/%m/%y"), amount)

#login = 'WQLXCYMEUZ'
#passw = 'BGdcN1G72e'