import sqlite3 as sq
from typing import Generator

"""

    sql_start() - инициализация базы данных:
        global var: base, cur
        table: menu {
                     name:          Название товара                 PRIMARY_KEY
                     description:   Описание товара
                     amount:        Кол-во доступного товара
                     price:         Цена товара
                    }
               orders{
                     id_person:     ID тг пользователя
                     wallet:        Кошелёк пользователя            PRIMARY_KEY(убирает возможность делать новый заказ
                                                                                с этим кошельком до оплаты 
                                                                                предыдущего товара)
                                                                                 
                     name:          Название выбранного товара
                     amount:        Количество выбранного товара
                     flag:          Флаг проверки оплаты
                                    (по умолчанию=False)
                     } 
               users {
                     id_person:     ID тг пользователя
                     wallet:        Кошелёк пользователя            PRIMARY_KEY
                     name:          Название выбранного товара
                     amount:        Количество выбранного товара
                     }
               

    sql_menu() - вывод всех данных из таблицы menu
    sql_orders() - вывод всех данных из таблицы orders
    sql_users() - вывод всех данных из таблицы users
    sql_selected_user_orders() - вывод данных об активных заказах пользователя
    
    sql_add_products() - добавление новых продуктов в базу данных
    sql_add_orders() - добавление новых записей о заказах в таблицу orders
    sql_add_users() - добавление новых записей о пользователях в таблицу users
    
    sql_del_orders() - проверка оплаты и удаление заказа из таблицы orders
    sql_check_adequacy() - проверка наличия выбранного товара и количества
    sql_check() - проверка flag из таблицы orders на значение True
    
    q
"""


# добавить документацию - VX
# ещё бы сделать проверку адреса по маске - Х
# узнать как делать аннотации для бд - ХЗ
# после создания рабочей конструкции сделать поиск исключений - Х

# daaat = ('1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2', 'ROW', 2, False)

def sql_start() -> None:
    global base, cur
    base = sq.connect(r'crypto_market.db')  # поиск и создание файла бд
    cur = base.cursor()  # курсор для взаимодействия с бд
    if base:
        print('Data base connected OK!')
    cur.execute('CREATE TABLE IF NOT EXISTS menu('
                'name TEXT PRIMARY KEY,'
                'description TEXT,'
                'amount INTEGER,'
                'price TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS users('
                'id_person INTEGER,'
                'wallet TEXT PRIMARY KEY,'
                'name TEXT,'
                'amount INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS orders('
                'id_person INTEGER,'
                'wallet TEXT PRIMARY KEY,'
                'name TEXT,'
                'amount INTEGER,'
                'flag BLOB)')

    # execute - отвечает за sql запрос
    # создаётся таблица, если её не было. Дальше разграничиваем бд
    base.commit()  # cохраняем изменения


# ВЫВОД
def sql_menu() -> Generator:
    # для красивого вывода:
    print('\nMENU:')
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        print('\n\tNAME:', ret[0], '\n\tDESCRIPTION:', ret[1], '\n\tAMOUNT:', ret[2], '\n\tPRICE:', ret[3])

    # для передачи в виде списка:
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        yield ret


def sql_orders() -> Generator:
    # для красивого вывода:
    print('\nORDERS:')
    for ret in cur.execute('SELECT * FROM orders').fetchall():
        print('\n\tID_PERSONE:', ret[0], '\n\tWALLET:', ret[1], '\n\tNAME:', ret[2], '\n\tAMOUNT:', ret[3], '\n\tFLAG:',
              ret[4])

    # для передачи в виде списка:
    for ret in cur.execute('SELECT * FROM orders').fetchall():
        yield ret


def sql_users() -> Generator:
    # для красивого вывода:
    print('\nUSERS:')
    for ret in cur.execute('SELECT * FROM users').fetchall():
        print('\n\tID_PERSONE:', ret[0], '\n\tWALLET:', ret[1], '\n\tNAME:', ret[2], '\n\tAMOUNT:', ret[3])

    # для передачи в виде списка:
    for ret in cur.execute('SELECT * FROM users').fetchall():
        yield ret


def sql_selected_user_orders(user_id: int) -> list:
    r = cur.execute('SELECT * FROM users WHERE id_person == {}'.format(user_id)).fetchall()
    for i_elem in r:
        yield i_elem


# ДОБАВЛЕНИЕ
def sql_add_product(lst: tuple) -> None:
    cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', *lst)
    base.commit()


def sql_add_orders(lst: tuple) -> None:
    cur.execute('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', (*lst, False))
    base.commit()


def sql_add_users(lst: tuple) -> None:
    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?)', *lst)
    base.commit()


# ПРОВЕРКИ
def sql_del_orders(wal: str) -> None:
    if sql_check(wal):
        cur.execute('DELETE FROM orders WHERE wallet=? ', (wal,))
        base.commit()
        print('ПОЛУЧИЛОСЬ!')
    else:
        print('Ну почти')


def sql_check_adequacy(user_id: int) -> None:
    r = cur.execute('SELECT * FROM users WHERE id_person == {}'.format(user_id)).fetchall()
    print(*r)
    for i_elem in r:
        if cur.execute('SELECT name FROM menu WHERE name=? and amount=?', (i_elem[2], i_elem[3])):
            print('ПОЛУЧИЛОСЬ!', *i_elem)
            sql_add_orders(i_elem)
        else:
            print('Выберите другое количество товара!')


def sql_check(wal: str) -> bool:
    if cur.execute('SELECT wallet FROM orders WHERE flag=? and wallet=?', (True, wal)):
        return True
    else:
        return False


sql_start()
# sql_check()
# sql_add_product('ASD', 'COLE', 1234, 1234)
# sql_check_adequacy(2112523)
# print(sql_check_user_orders(2112523))
# sql_menu()
# sql_users()
print(list(sql_orders()))
sql_check('3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy')
sql_del_orders('3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy')
print(list(sql_selected_user_orders(2112523)))
