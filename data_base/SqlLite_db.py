import logging
import sqlite3 as sql
import sys
import time
from datetime import datetime
from logging import StreamHandler, Formatter
from random import uniform

from data_base import payments_func

# psycopg2-binary

"""
  sql_start() - инициализация базы данных

  add_user(user_id:int, username:str, email:str) - добавление нового пользователя, если есть, то принтует об этом

  add_products(key: str, name: str, description: str, amount: int, price: int, logo: int) - добавление новых продуктов, 
                                                если такой ключ уже существует, то просто апдейтим данные на этот ключ

  add_orders(id_user: int, id_prod: int, amount: int) - добавление заказа (уникальности не требует)

  add_history(id_hash: str, curr_order: int) - добавление заказа в историю (уникальности не требует) 

  get_all_products(choice:int) - выборка продуктов из бд. По-умолчанию все продукты. Чтобы вывести конкретный - передать 
                                 существующий в таблице айди продукта  

  show_lk(choice='*', user_id=('*',)) - выборка полей таблицы LK. По-умолчанию все поля и все пользователи.
                                        Чтобы вывести конкретное поле и пользователя - передать 

"""

try:
    logger = logging.getLogger("exampleApp")
    logger.setLevel(logging.DEBUG)

    handler = StreamHandler(stream=sys.stdout)


    def db_start():
        global con, cur
        try:
            con = sql.connect(database="../data_base/crypto")  # имя ДБ, к которой мы подключаемся
            cur = con.cursor()
            handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
            logger.addHandler(handler)
            logger.debug('DATABASE OPEN SUCCESSFULLY')
        except Exception as e:
            print(e)
        cur.execute('''CREATE TABLE IF NOT EXISTS products
             (id_products INTEGER PRIMARY KEY,
             key VARCHAR(100) NOT NULL,
             name VARCHAR(100) NOT NULL,
             description VARCHAR(200),
             amount INTEGER,
             price INTEGER NOT NULL,
             logo VARCHAR(200));''')
        cur.execute('''CREATE TABLE IF NOT EXISTS LK  
             (id_LK INTEGER CONSTRAINT LK_id PRIMARY KEY NOT NULL,
             balance DECIMAL(12,2) CONSTRAINT LK_balance_check CHECK(balance>=0) DEFAULT 0,
             hist VARCHAR(200) DEFAULT 0);''')
        cur.execute('''CREATE TABLE IF NOT EXISTS orders  
             (id_orders INTEGER PRIMARY KEY AUTOINCREMENT,
             id_user INTEGER NOT NULL,
             id_products INTEGER NOT NULL,
             amount INTEGER,
             amount_payable INTEGER NOT NULL);''')
        cur.execute('''CREATE TABLE IF NOT EXISTS history  
             (id_user INTEGER NOT NULL,
             sum INTEGER NOT NULL,
             date DATE NOT NULL,
             flag BLOB DEFAULT 0);''')
        cur.execute('''CREATE TABLE IF NOT EXISTS main_balance
             (balance INTEGER NOT NULL);''')
        handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
        logger.addHandler(handler)
        logger.debug('DATABASE CREATED')
        con.commit()


    def first_seen(user_id: int):
        try:
            cur.execute("SELECT id_LK FROM LK WHERE id_LK=?", (user_id,))
            res = cur.fetchall()
            if not res:
                cur.execute('INSERT INTO LK VALUES (?,?,?);',
                            (user_id, 0, 0))
                handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
                logger.addHandler(handler)
                logger.debug('THE USER ADDED TO THE DATABASE')
                con.commit()
                return True
            else:
                handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
                logger.addHandler(handler)
                logger.debug('THE USER IS IN THE DATABASE')
                return False
        except Exception as e:
            print(e)


    def add_products(key: str, name: str, description: str, amount: int, price: int, logo: int):
        try:
            if not cur.execute('SELECT * FROM products WHERE key=?', [key]):
                cur.execute(
                    'INSERT INTO products (key, name, description, amount, price, logo) VALUES(?, ?, ?, ?, ?, ?);',
                    (key, name, description, amount, price, logo))
            else:
                cur.execute(
                    'UPDATE products SET name=?, description=?, amount=?, price=?, logo=? WHERE key=?;',
                    (name, description, amount, price, logo, key))
                # запрашивать у пользователя разрешение на UPDATE, или сразу делать
            con.commit()
        except Exception as e:
            print(e)


    def add_orders(id_user: int, id_prod: int, amount: int):
        if cur.execute('SELECT * FROM lk WHERE id_lk=?', [id_user]):
            cur.execute('SELECT price FROM products WHERE id_products=?', [id_prod])
            total = cur.fetchone()[0] * amount
            cur.execute('INSERT INTO orders (id_user, id_products, amount, amount_payable) VALUES(?, ?, ?, ?);',
                        (id_user, id_prod, amount, total))
            con.commit()
        else:
            print('Такого пользователя нет.')
            raise Exception


    def get_all_products(choice=-1):  # можно делать через свой курсор
        dima_dict = {}
        if choice == -1:
            cur.execute('SELECT * FROM products')
        else:
            cur.execute('SELECT * FROM products WHERE id_products=?', [choice])
        for elem in cur.fetchall():
            dima_dict[elem[1]] = {'id': f'{elem[0]}',
                                  'name': f'{elem[2]}', 'description': f'{elem[3]}',
                                  'amount': f'{elem[4]}',
                                  'price': f'{elem[5]}', 'logo': f'{elem[6]}'}

        return dima_dict


    def show_lk(choice='*', user_id=0):
        try:
            if choice == '*' and user_id == 0:
                cur.execute('SELECT DISTINCT * FROM lk;')
            else:
                sqlstring = f'SELECT DISTINCT {choice} FROM lk WHERE id_lk ={user_id};'
                cur.execute(f'{sqlstring}')
            return cur.fetchall()[0]
        except Exception as e:
            print(e)


    # sup
    def search_by_orders(id_u):
        res = 0
        cur.execute('SELECT amount_payable FROM orders WHERE id_user=?', (id_u,))
        r = cur.fetchall()
        for i in r:
            for n in i:
                res += n
        return res


    def payments_create(id_u: int):
        summ = search_by_orders(id_u)
        payment = summ + uniform(0.001, 0.005)  # sum randomize
        date = datetime.today().strftime('%Y-%m-%d %H:%M')  # date warning

        while round(payment, 4) is cur.execute('SELECT amount_payable FROM orders WHERE id_user=?', (id_u,)):
            payment = summ + uniform(0.001, 0.005)
        payment = round(payment, 4)
        if not cur.execute('SELECT * FROM history WHERE id_user=?', (id_u,)):
            cur.execute('INSERT INTO history VALUES (?,?,?,?)', (id_u, payment, date, 0))
            con.commit()
        else:
            logger.addHandler(handler)
            logger.debug('THIS USER HAS ALREADY ORDERED')


    def balance_vis(id_u):
        flag = False
        cur.execute('SELECT sum FROM history WHERE id_user=?', (id_u,))
        needed = int(cur.fetchall()[0][0])

        balance_cur = payments_func.get_balance()
        needed += balance_cur
        while True:
            if payments_func.get_balance() == needed:
                cur.execute('UPDATE history SET flag=? WHERE id_user=?', (True, id_u))
                flag = True
                con.commit()
                return flag
            time.sleep(100)


    db_start()
    first_seen(13)
    # print(get_addr_key(13))
    payments_create(1)

except Exception as TotalError:
    print("Ошибка при работе с SQLite3:", TotalError, end='\n')
    # finally:
    #     if __name__ == '__main__':
    #         con.close()
    print('База данных закрыта')