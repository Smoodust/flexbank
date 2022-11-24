from random import randrange
import hashlib

users = [('Гончарова', 'Маргарита', 'Данииловна', 85455575084, '5/8/1990'), ('Кондратьев', 'Семён', 'Тимофеевич', 85879356184, '3/7/1993'), ('Васильев', 'Артём', 'Ильич', 82066332958, '7/10/1986'), ('Ильина', 'Есения', 'Николаевна', 85994505079, '1/11/2000'), ('Сорокин', 'Семён', 'Дмитриевич', 89636957782, '7/8/1992'), ('Черкасова', 'София', 'Львовна', 80899247036, 
'3/1/2001'), ('Сидорова', 'Элина', 'Матвеевна', 83165985429, '9/2/1999'), ('Михайлова', 'Александра', 'Олеговна', 89202414851, '10/6/1999'), ('Чернышева', 'Дарья', 'Леонидовна', 82039650668, '8/1/2001'), ('Козина', 'Светлана', 'Максимовна', 81922281115, '11/5/1982')]
logins = ['QQKGJFPVFY', 'WQLXCYMEUZ', 'FGYZQVWSNS', 'TNQRQGZWDB', 'NLJDQKYSSR', 'UOWXLWJFCB', 'MFAFJDZJTH', 'CPNCGDDYLP', 'YYPRYAKWWA', 'YZDLPBTSDY']
passwords = ['FociSsQIb8', 'BGdcN1G72e', 'bAx9Jq8f4f', 'TsdGuGx0Sh', '6PZ4FyjB8L', 'ttEP2XtV3I', 'TLOEkC7Vqm', 'l4gPdrN9Ik', 'Z3wp7vobZn', '773cyOaEEo']
passwords = [hashlib.sha256(x.encode('utf-8')).hexdigest() for x in passwords]
#card_number = [2, 1, 3, 1, 2, 1, 1, 2, 1, 1]

print([[*users[i], logins[i], passwords[i]] for i in range(10)])
#print([[[u, ] if i == 0 for i in range(x)] for u, x in enumerate(card_number)])