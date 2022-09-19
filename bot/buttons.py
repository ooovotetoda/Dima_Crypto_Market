from aiogram.types import InlineKeyboardButton

from texts import StatesMsg

personal_cabinet = InlineKeyboardButton(text=StatesMsg.personal_cabinet.get("button"), callback_data=StatesMsg.personal_cabinet.get("callback"))
deposit = InlineKeyboardButton(text=StatesMsg.deposit.get("button"), callback_data=StatesMsg.deposit.get("callback"))
crypto = InlineKeyboardButton(text=StatesMsg.crypto.get("button"), callback_data=StatesMsg.crypto.get("callback"))
fiat = InlineKeyboardButton(text=StatesMsg.fiat.get("button"), callback_data=StatesMsg.fiat.get("callback"))
check_transaction = InlineKeyboardButton(text=StatesMsg.check_transaction.get("button"), callback_data=StatesMsg.check_transaction.get("callback"))
purchase_history = InlineKeyboardButton(text=StatesMsg.purchase_history.get("button"), callback_data=StatesMsg.purchase_history.get("callback"))
balance_history = InlineKeyboardButton(text=StatesMsg.balance_history.get("button"), callback_data=StatesMsg.balance_history.get("callback"))
support = InlineKeyboardButton(text=StatesMsg.support.get("button"), callback_data=StatesMsg.support.get("callback"))
products = InlineKeyboardButton(text=StatesMsg.products.get("button"), callback_data=StatesMsg.products.get("callback"))


BUTTONS = {
    "personal_cabinet": personal_cabinet,
    "deposit": deposit,
    "crypto": crypto,
    "fiat": fiat,
    "check_transaction": check_transaction,
    "purchase_history": purchase_history,
    "balance_history": balance_history,
    "support": support,
    "products": products,
}
