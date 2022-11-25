status_to_string = {
    'active':'активный',
    'blocked':'заблокированый',
    'closed':'закрытый'
}

type_to_string = {
    'debit':'дебитовый',
    'credit':'кредитный',
}

concrete_account_first = '''Счет {}
Информация:
Баланс - {:.2f}₽
Кол-во привязанных карт - {}'''