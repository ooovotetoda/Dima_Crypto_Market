import sqlite3 as sql
from datetime import datetime

# psycopg2-binary
# убрать принты. Пока они нужны, чтобы понимать что и куда

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
    def db_start():
        global con, cur
        con = sql.connect(database="crypto")  # имя ДБ, к которой мы подключаемся
        cur = con.cursor()
        print("Database opened successfully")
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
             username VARCHAR(30), 
             email VARCHAR(30),
             balance DECIMAL(12,2) CONSTRAINT LK_balance_check CHECK(balance>=0) DEFAULT 0,
             cur_orders INTEGER DEFAULT 0,
             hist VARCHAR(200) DEFAULT 0,
             address VARCHAR(100),
             wif VARCHAR(100));''')
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
        cur.execute('''CREATE TABLE IF NOT EXISTS busy_wallets
                     (id_person TEXT,
                     wallet TEXT PRIMARY KEY,
                     coin TEXT);''')
        con.commit()


    def add_users(user_id: int, username: str, email: str):
        try:
            if not cur.execute('SELECT * FROM lk WHERE id_lk=?', [user_id]):
                cur.execute('INSERT INTO lk (id_lk, username, email) VALUES(?, ?, ?);', (user_id, username, email))
            else:
                print('Такой пользователь уже существует')
                raise Exception
            con.commit()
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


    def add_free_wallet(id_cur, wallet, coin):
        cur.execute('INSERT INTO busy_wallets VALUES(?,?,?);', (id_cur, wallet, coin))
        con.commit()


    def select_wallet(coin):
        return cur.execute('SELECT * FROM busy_wallets WHERE coin=?', (coin,))


    def select_wallet_count(coin):
        return list(cur.execute('SELECT COUNT(*) FROM busy_wallets WHERE coin=?', (coin,)).fetchone())


    db_start()
    # add_users(user_id=124125, username='Booblya', email='qweyu@mail.ru')
    # add_products('Skit', 'КОТАН', 'вот такое животное', 100, 10101, 1488)
    # add_orders(124125, 1, 5)
    # add_history('qweqwrhfhfqwe21312@21311', 1)
    # print(get_all_products(-1))
    # print(show_lk(choice='email', user_id=124125))
    # print(show_lk())


except Exception as TotalError:
    print("Ошибка при работе с SQLite3:", TotalError, end='\n')
    # finally:
    #     if __name__ == '__main__':
    #         con.close()
    print('База данных закрыта')