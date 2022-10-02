from products_list import available_products
from data_base.wallet_functions import gen_address
from data_base.SqlLite_db import get_from_lk

public, private = gen_address(0)

prods = []
for key, val in available_products.items():
    prods.append(key)

class StatesMsg:
    start = {"message": "Это бот для оплаты криптовалютами!",
             "button": "",
             "callback": "products",
             "keyboard": ["products", "personal_cabinet", "support"]}

    products = {"message": "Все товары",
                "button": "Товары",
                "callback": "products",
                "keyboard": prods}

    go_pay = {"message": f"Адрес для перевода:<b>\n{public}\n\n</b>"
                        f"{get_from_lk()}",
             "button": "Перейти к оплате",
             "callback": "go_pay",
             "keyboard": ["check_transaction"]}

    personal_cabinet = {"message": "Это ваш личный кабинет",
                        "button": "Личный кабинет",
                        "callback": "personal_cabinet",
                        "keyboard": ["purchase_history"]}

    # deposit = {"message": "Выберете способ оплаты",
    #            "button": "Пополнить баланс",
    #            "callback": "deposit",
    #            "keyboard": ["crypto", "fiat"]}

    # crypto = {"message": "Оплата криптовалютами",
    #           "button": "Криптовалюты",
    #           "callback": "deposit_crypto",
    #           "keyboard": []}

    # fiat = {"message": "*Подключаем робокассу*",
    #         "button": "Фиат",
    #         "callback": "deposit_fiat",
    #         "keyboard": []}

    check_transaction = {"message": "*Проверяем транзакцию*",
                         "button": "Проверить транзакцию",
                         "callback": "check_transaction",
                         "keyboard": []}

    purchase_history = {"message": "*История покупок, товары, даты и тд*",
                        "button": "История покупок",
                        "callback": "purchase_history",
                        "keyboard": ["support"]}

    # balance_history = {"message": "*История баланса пользователя*",
    #                    "button": "История баланса",
    #                    "callback": "balance_history",
    #                     "keyboard": ["support"]}

    support = {"message": "Не грусти, брат. Всё будет хорошо)",
               "button": "Поддержка",
               "callback": "support",
               "keyboard": []}

    product = {"message": "Текст товара",
               "button": "Название товара",
               "callback": "product",
               "keyboard": ["go_pay"]}