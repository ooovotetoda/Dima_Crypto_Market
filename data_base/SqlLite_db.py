import logging
import sqlite3 as sql
import sys
from datetime import datetime
from logging import StreamHandler, Formatter
import dump

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
             cur_orders INTEGER DEFAULT 0,
             hist VARCHAR(200) DEFAULT 0,
             state BLOB DEFAULT TRUE,
             address VARCHAR(100) DEFAULT 0,
             address_hex VARCHAR(100),
             private_key VARCHAR(100),
             public_key VARCHAR(100));''')
        cur.execute('''CREATE TABLE IF NOT EXISTS orders  
             (id_orders INTEGER PRIMARY KEY,
             id_user INTEGER NOT NULL,
             id_products INTEGER NOT NULL,
             amount INTEGER,
             amount_payable INTEGER NOT NULL);''')
        cur.execute('''CREATE TABLE IF NOT EXISTS history  
             (id_hash TEXT NOT NULL,
             id_orders INTEGER NOT NULL,
             id_users INTEGER NOT NULL,
             id_products INTEGER NOT NULL,
             sum INTEGER NOT NULL,
             date DATE NOT NULL);''')
        handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
        logger.addHandler(handler)
        logger.debug('DATABASE CREATED')
        con.commit()


    def first_seen(user_id: int):
        try:

            cur.execute("SELECT id_LK FROM LK WHERE id_LK=?", (user_id,))
            res = cur.fetchall()

            if not res:
                cur.execute('INSERT INTO LK VALUES (?,?,?,?,?,?,?,?,?);',
                            (user_id, 0, 0, 0, True, *list(dump.gen_address())))
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


    def add_history(id_hash: str, curr_order: int):
        try:
            if cur.execute('SELECT * FROM orders'):
                cur.execute(
                    '''SELECT orders.id_user as users, orders.id_products as products , orders.amount_payable as amount 
                    FROM orders WHERE id_orders =?''',
                    [curr_order])
                record = cur.fetchone()
                date = datetime.today().strftime('%Y-%m-%d %H:%M')
                cur.execute('INSERT INTO history VALUES(?, ?, ?, ?, ?, ?);',
                            (id_hash, curr_order, record[0], record[1], record[2], date))
                con.commit()
            else:
                print('Пустая БД')
                raise Exception
        except Exception as e:
            print(e)


    def get_all_products(choice=-1):  # можно делать через свой курсор
        danya_dict = {}
        if choice == -1:
            cur.execute('SELECT * FROM products')
        else:
            cur.execute('SELECT * FROM products WHERE id_products=?', [choice])
        for elem in cur.fetchall():
            danya_dict[elem[1]] = {'id': f'{elem[0]}',
                                   'name': f'{elem[2]}', 'description': f'{elem[3]}',
                                   'amount': f'{elem[4]}',
                                   'price': f'{elem[5]}', 'logo': f'{elem[6]}'}

        return danya_dict


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


    def get_addr_key(id_u):
        cur.execute(f'SELECT address, address_hex, private_key, public_key FROM LK WHERE id_LK=?', (id_u,))
        return list(cur.fetchone())


    def send(id_u, to_wallet):
        try:
            w = get_addr_key(id_u)
            amount = dump.get_balance(w[0], 'USDT')
            dump.send_tron(w[0], w[1], to_wallet, float(amount))
        except Exception as e:
            print(e)


    db_start()
    first_seen(11)
    print(get_addr_key(11))
    print(send(11, 'TD8iW5o5qF5L9EkYRfKqcxU1S7MrmvdZ6M'))


except Exception as TotalError:
    print("Ошибка при работе с SQLite3:", TotalError, end='\n')
    # finally:
    #     if __name__ == '__main__':
    #         con.close()
    print('База данных закрыта')
