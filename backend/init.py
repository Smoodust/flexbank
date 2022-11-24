import sqlite3 as sl

def get_connection():
    return sl.connect('C:/Users/USER/Documents/flexbank/database/database.db')

conn = get_connection()
cursor = conn.cursor()
cursor.execute('''CREATE TABLE USER (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, surname TEXT, name TEXT, patronymic TEXT, phone INTEGER, date_of_birth TEXT, login)''')
cursor.execute('''CREATE TABLE CARDS (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id_user INTEGER, type TEXT, card_number TEXT, validity_period TEXT, cvc INTEGER)''')
users = [['Гончарова', 'Маргарита', 'Данииловна', 85455575084, '5/8/1990', 'QQKGJFPVFY', '9d2a42f9728e768d68c3d21a2b9348d3199026721cc9b787e4acd6fb3f9b63b2'], ['Кондратьев', 'Семён', 'Тимофеевич', 85879356184, '3/7/1993', 'WQLXCYMEUZ', 'b646e398b3098aaf6e030c1b2ccdd2fa747726fd0de4a25acc07906fb93b65e2'], ['Васильев', 'Артём', 'Ильич', 82066332958, '7/10/1986', 'FGYZQVWSNS', '374becf762a965479a354ea5dcfa362362b36162d44ce1211c13674d5e8fb4c2'], ['Ильина', 'Есения', 'Николаевна', 85994505079, '1/11/2000', 'TNQRQGZWDB', '5241b233d41db6a500e2d906782eb2dd3a6d77528f26f65ed585c53c28f3108b'], ['Сорокин', 'Семён', 'Дмитриевич', 89636957782, '7/8/1992', 'NLJDQKYSSR', 'f5603adf70d7699d5edca9b84f2a7da87fe5acbc267f8c9f63250a3c0d1b4d25'], ['Черкасова', 'София', 'Львовна', 80899247036, '3/1/2001', 'UOWXLWJFCB', '8f2904ac243595258bab0ff4623f5796a1deeb97574491a36917051e3162e6c9'], ['Сидорова', 'Элина', 'Матвеевна', 
83165985429, '9/2/1999', 'MFAFJDZJTH', 'ac32dfebbc19f705b283eb509de0e96af13eef1610332f8b25adab93a16684d7'], ['Михайлова', 'Александра', 'Олеговна', 89202414851, '10/6/1999', 'CPNCGDDYLP', '4f888c5204541b8ceb5150bf003a116e48a3586b1f4bbe6149268d746546c94e'], ['Чернышева', 'Дарья', 'Леонидовна', 82039650668, '8/1/2001', 'YYPRYAKWWA', 'a9a8a4ff5139bb6165886dee998390761d9e085f50c88ad833078deab14a592d'], ['Козина', 'Светлана', 'Максимовна', 81922281115, '11/5/1982', 'YZDLPBTSDY', '741cf35ada9d2b56c8d8167d8860f2cc74938bdd3b3cd9d13dc3e2cd3d0dfb5f']]
cursor.executemany('INSERT INTO USER (surname, name, patronymic, phone, date_of_birth) values(?,?,?,?,?)', users)
conn.commit()
conn.close()