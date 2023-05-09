from db import sqlite


def insert_order(order):
    sql = ''' INSERT INTO order_management 
        (user_id, ticker_symbol, net_cost, action, status, price_type, date, message_details) 
        VALUES(?,?,?,?,?,?,?,?) '''
    return sqlite.insert(order, sql)


def update_account(order):
    sql = '''UPDATE order_management 
        SET user_id = ?, ticker_symbol = ?, net_cost=?, action=?, status=?, price_type=?, date=?, message_details=?
        WHERE user_id = ?'''
    sqlite.update(order, sql)


def select_all():
    sql = 'SELECT * from order_management'
    return sqlite.select_all(sql)


def select_by_user_id(user_id):
    sql = 'SELECT * from order_management WHERE user_id = ?'
    return sqlite.select_by_key(user_id, sql)


def delete_all():
    sql = 'DELETE from order_management'
    sqlite.delete_all(sql)


def delete_by_user_id(user_id):
    sql = 'DELETE FROM order_management WHERE user_id = ?'
    sqlite.delete_by_key(user_id, sql)
