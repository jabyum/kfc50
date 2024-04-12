import sqlite3
from datetime import datetime
connection = sqlite3.connect("kfc.db")
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, "
            "name TEXT, phone_number TEXT, reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pr_name TEXT,  pr_price REAL, pr_quantity INTEGER, pr_des TEXT,"
            "pr_photo TEXT, reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, pr_id INTEGER, "
            "pr_name TEXT, pr_count INTEGER, total_price REAL);")
connection.commit()

def add_user(user_id, name, phone_number):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO users (user_id, name, phone_number,"
                "reg_date) VALUES (?,?,?,?);", (user_id, name,
                                                phone_number, datetime.now()))
    connection.commit()
def check_user(user_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    # пробуем вытащить пользователя из базы данных по его айди
    checker = sql.execute("SELECT user_id FROM users "
                          "WHERE user_id=?;", (user_id, )).fetchone()
    # если мы его нашли в базе данных
    if checker:
        return True
    # если не нашли в бд
    return False
def get_all_users():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    users = sql.execute("SELECT * FROM users;").fetchall()
    return users

def add_product(pr_name, pr_quantity, pr_price, pr_des, pr_photo):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO products (pr_name, pr_price, pr_quantity, "
                "pr_des, pr_photo, reg_date) VALUES (?,?,?,?,?,?);",
                (pr_name, pr_price, pr_quantity, pr_des, pr_photo, datetime.now()))
    connection.commit()
def get_all_products():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_products = sql.execute("SELECT * FROM products;").fetchall()
    return all_products
def get_exact_produdct(pr_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    exact_product = sql.execute("SELECT pr_name, pr_price, pr_des, pr_photo FROM products "
                                "WHERE pr_id=?;", (pr_id, )).fetchone()
    return exact_product
def get_pr_id_name():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_products = sql.execute("SELECT pr_id, pr_name, pr_quantity FROM products;").fetchall()
    actual_products = [(i[0], i[1]) for i in all_products if i[2]>0]
    return actual_products
def get_all_id():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_id = sql.execute("SELECT pr_id FROM products;").fetchall()
    actual_id = [i[0] for i in all_id]
    return actual_id
def delete_products():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products;")
    connection.commit()
    return get_all_products()
def delete_exact_products(pr_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products WHERE pr_id=?;", (pr_id, ))
    connection.commit()
def change_quantity(pr_id, new_quantity):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("UPDATE products SET pr_quantity=? WHERE pr_id=?;",
                (new_quantity, pr_id))
    connection.commit()
# корзина
def add_to_cart(user_id, pr_id, pr_name, pr_count, pr_price):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    total_price = pr_count * pr_price
    sql.execute("INSERT INTO cart (user_id, pr_id, pr_name, pr_count, total_price) "
                "VALUES (?,?,?,?,?);", (user_id, pr_id, pr_name,
                                        pr_count, total_price))
    connection.commit()

# удаление продукта из корзины
def delete_exact_pr_from_cart(user_id, pr_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM cart WHERE user_id=? AND pr_id=?;", (user_id, pr_id))
    connection.commit()

# получение корзины пользователя (fetchall())
def get_user_cart(user_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    user_cart = sql.execute("SELECT pr_name, pr_count, total_price FROM cart "
                            "WHERE user_id=?;", (user_id,)).fetchall()
    return user_cart
# очистить корзину
def delete_user_cart(user_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM cart WHERE user_id=?;", (user_id, ))
    connection.commit()
def delete_exact_product_from_cart(user_id, pr_name):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM cart WHERE user_id=? and pr_name=?;", (user_id, pr_name))
    connection.commit()
def get_cart_id_name(user_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    user_cart = sql.execute("SELECT pr_name, pr_id FROM cart "
                            "WHERE user_id=?;", (user_id,)).fetchall()
    return user_cart
