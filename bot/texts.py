class MESSAGE_TXT:
    start = "Это бот для оплаты криптовалютами!"
    personal_cabinet = "Это ваш персональный кабинет"
    deposit = "Выберете способ оплаты"
    crypto = "Оплата криптовалютами"
    fiat = "*Подключаем робокассу*"
    check_transaction = "Нажмите кнопку для подтверждения транзакции"
    purchase_history = "*История покупок, товары, даты и тд*"
    balance_history = "*История баланса пользователя*"
    support = "Не грусти, брат. Всё будет хорошо)"

class BUTTONS_TXT:
    personal_cabinet = "Личный кабинет"
    deposit = "Пополнить баланс"
    crypto = "Криптовалюты"
    fiat = "Фиат"
    check_transaction = "Проверить транзакцию"
    purchase_history = "История покупок"
    balance_history = "История баланса"
    support = "Поддержка"
    # back = "Назад"


class CALLBACK_TXT:
    personal_cabinet = "personal_cabinet"
    deposit = "deposit"
    crypto = "deposit_crypto"
    fiat = "deposit_fiat"
    check_transaction = "check_transaction"
    purchase_history = "purchase_history"
    balance_history = "balance_history"
    support = "support"
    # back = "back"

class KEYBOARDS:
    start = ["personal_cabinet", "support"]
    personal_cabinet = ["deposit", "purchase_history", "balance_history"]
    deposit = ["crypto", "fiat"]
    crypto = []
    fiat = []
    check_transaction = ["check_transaction"]
    purchase_history = ["support"]
    balance_history = ["support"]
    support = []


