from aiogram.types import InlineKeyboardButton

from texts import CALLBACK_TXT, BUTTONS_TXT

personal_cabinet = InlineKeyboardButton(text=BUTTONS_TXT.personal_cabinet, callback_data=CALLBACK_TXT.personal_cabinet)
deposit = InlineKeyboardButton(text=BUTTONS_TXT.deposit, callback_data=CALLBACK_TXT.deposit)
crypto = InlineKeyboardButton(text=BUTTONS_TXT.crypto, callback_data=CALLBACK_TXT.crypto)
fiat = InlineKeyboardButton(text=BUTTONS_TXT.fiat, callback_data=CALLBACK_TXT.fiat)
check_transaction = InlineKeyboardButton(text=BUTTONS_TXT.check_transaction, callback_data=CALLBACK_TXT.check_transaction)
purchase_history = InlineKeyboardButton(text=BUTTONS_TXT.purchase_history, callback_data=CALLBACK_TXT.purchase_history)
balance_history = InlineKeyboardButton(text=BUTTONS_TXT.balance_history, callback_data=CALLBACK_TXT.balance_history)
support = InlineKeyboardButton(text=BUTTONS_TXT.support, callback_data=CALLBACK_TXT.support)
# back = InlineKeyboardButton(text=BUTTONS_TXT.back, callback_data=CALLBACK_TXT.back)


BUTTONS = {
    "personal_cabinet": personal_cabinet,
    "deposit": deposit,
    "crypto": crypto,
    "fiat": fiat,
    "check_transaction": check_transaction,
    "purchase_history": purchase_history,
    "balance_history": balance_history,
    "support": support,
    # "back": back,
}
