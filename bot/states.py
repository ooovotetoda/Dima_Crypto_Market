from texts import StatesMsg
from keyboard import get_keyboard
from products_list import available_products

class Mess:
    def __init__(self, text_state, keyboard, prev_state):
        self.text_state = text_state
        self.keyboard = get_keyboard(keyboard, prev_state)
        self.prev_state = prev_state


states = {
    "start":             Mess(StatesMsg.start.get("message"), StatesMsg.start["keyboard"], None),
    "products":          Mess(StatesMsg.products.get("message"), StatesMsg.products["keyboard"], "start"),
    "go_pay":            Mess(StatesMsg.go_pay.get("message"), StatesMsg.go_pay["keyboard"], "start"),
    "personal_cabinet":  Mess(StatesMsg.personal_cabinet.get("message"), StatesMsg.personal_cabinet["keyboard"], "start"),
    # "deposit":           Mess(StatesMsg.deposit.get("message"), StatesMsg.deposit["keyboard"], "personal_cabinet"),
    # "deposit_crypto":    Mess(StatesMsg.crypto.get("message"), StatesMsg.crypto["keyboard"], "deposit"),
    # "deposit_fiat":      Mess(StatesMsg.fiat.get("message"), StatesMsg.fiat["keyboard"], "deposit"),
    "check_transaction": Mess(StatesMsg.check_transaction.get("message"), StatesMsg.check_transaction["keyboard"], "go_pay"),
    "purchase_history":  Mess(StatesMsg.purchase_history.get("message"), StatesMsg.purchase_history["keyboard"], "personal_cabinet"),
    # "balance_history":   Mess(StatesMsg.balance_history.get("message"), StatesMsg.balance_history["keyboard"], "personal_cabinet"),
    "support":           Mess(StatesMsg.support.get("message"), StatesMsg.support["keyboard"], "start"),
}

#Добавляю стейты всех товаров
for key, val in available_products.items():
    states = states | {f'{key}': Mess(val.get('description'), StatesMsg.product.get("keyboard"), "products")}
