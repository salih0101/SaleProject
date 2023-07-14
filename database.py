import sqlite3


connection = sqlite3.connect('teledata.db')
sql = connection.cursor()


def add_user(user_id, name, phone_number, time_sub, end_sub, status, amount_sub):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO "users" VALUES (?,?,?,?,?,?,?);', (user_id, name, phone_number, time_sub, end_sub, status, amount_sub))

    connection.commit()

    return add_user


def add_products_to_db(user_id, model, stated, color, storage, docs, price, address, number, telegramm, picture):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()
    sql.execute("INSERT INTO products VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (user_id, model, stated, color, storage, docs, price, address, number, telegramm, picture))
    connection.commit()


def get_users():

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()
    users = sql.execute('SELECT name, id, gender FROM users;')

    return users.fetchall()



def get_products_from_db(current_product):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()
    products = sql.execute('SELECT * FROM products WHERE name=?;', (current_product, ))
    return products.fetchall()


def get_product_id_from_db():

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()
    product_id = sql.execute('SELECT id FROM products;')
    return product_id.fetchall()


def check_user(user_id):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT user_id FROM users WHERE user_id=?;', (user_id,))

    if checker.fetchone():
        return True
    else:
        return False



def get_all_info_product(current_product):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()

    all_products = sql.execute('SELECT * FROM products WHERE name=?;', (current_product, ))

    return all_products.fetchone()


def get_name_product(category_id):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()

    product_id = sql.execute('SELECT * FROM products WHERE id=?;', (category_id,))
    return product_id.fetchall()



import sqlite3

def get_models_category(category_id):
    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()

    # Выполнение запроса с передачей имени категории
    product_id = sql.execute('SELECT * FROM categories WHERE name=?;', (category_id,))
    result = product_id.fetchall()


    return result



def search_product(name):

    connection = sqlite3.connect('teledata.db')
    sql = connection.cursor()

    sql.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
    rows = sql.fetchall()

    return rows


# Запрос на создание таблицы

# sql.execute('CREATE TABLE users(user_id integer, name text, phone_number text, time_sub datetime, end_sub datetime, status text, amount_sub integer);')
# sql.execute(
#     'CREATE TABLE products (user_id integer, model INTEGER, stated text, color TEXT, storage TEXT, docs TEXT, price INTEGER, address TEXT, number INTEGER, telegram TEXT, picture TEXT);')
# sql.execute('CREATE TABLE cart (user_id INTEGER, product_name TEXT, user_number TEXT, product_price INTEGER, product_count INTEGER);')
# sql.execute(
#     'CREATE TABLE categories (name integer, id integer);')

