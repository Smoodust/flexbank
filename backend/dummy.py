import hashlib

logins = ['QQKGJFPVFY', 'WQLXCYMEUZ', 'FGYZQVWSNS', 'TNQRQGZWDB', 'NLJDQKYSSR', 'UOWXLWJFCB', 'MFAFJDZJTH', 'CPNCGDDYLP', 'YYPRYAKWWA', 'YZDLPBTSDY']
passwords = ['FociSsQIb8', 'BGdcN1G72e', 'bAx9Jq8f4f', 'TsdGuGx0Sh', '6PZ4FyjB8L', 'ttEP2XtV3I', 'TLOEkC7Vqm', 'l4gPdrN9Ik', 'Z3wp7vobZn', '773cyOaEEo']
passwords = [hashlib.sha256(x.encode('utf-8')).hexdigest() for x in passwords]