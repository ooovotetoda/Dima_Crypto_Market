from texts import MESSAGE_TXT, KEYBOARDS
from keyboard import get_keyboard
from products_list import available_products

class Mess:
    def __init__(self, text_state, keyboard, prev_state):
        self.text_state = text_state
        self.keyboard = get_keyboard(keyboard, prev_state)
        self.prev_state = prev_state


states = {
    "start":             Mess(MESSAGE_TXT.start, KEYBOARDS.start, None),
    "products":          Mess(MESSAGE_TXT.products, KEYBOARDS.products, "start"),
    "personal_cabinet":  Mess(MESSAGE_TXT.personal_cabinet, KEYBOARDS.personal_cabinet, "start"),
    "deposit":           Mess(MESSAGE_TXT.deposit, KEYBOARDS.deposit, "personal_cabinet"),
    "deposit_crypto":    Mess(MESSAGE_TXT.crypto, KEYBOARDS.crypto, "deposit"),
    "deposit_fiat":      Mess(MESSAGE_TXT.fiat, KEYBOARDS.fiat, "deposit"),
    "check_transaction": Mess(MESSAGE_TXT.check_transaction, KEYBOARDS.check_transaction, "deposit_crypto"),
    "purchase_history":  Mess(MESSAGE_TXT.purchase_history, KEYBOARDS.purchase_history, "personal_cabinet"),
    "balance_history":   Mess(MESSAGE_TXT.balance_history, KEYBOARDS.balance_history, "personal_cabinet"),
    "support":           Mess(MESSAGE_TXT.support, KEYBOARDS.support, "start"),
}

#Добавляю стейты всех товаров
for key, val in available_products.items():
    states = states | {f'{key}': Mess(val.get('description'), KEYBOARDS.product, "products")}

