from db import sqlite


def insert_account(order):
    sql = ''' INSERT INTO account_order_info (user_id, account_balance, date, gains_losses_daily) VALUES(?,?,?,?) '''
    return sqlite.insert(order, sql)


def update_account(order):
    sql = '''UPDATE account_order_info 
        SET user_id = ?, account_balance = ?, date=?, gains_losses_daily=? 
        WHERE user_id = ?'''
    sqlite.update(order, sql)


def select_all():
    sql = 'SELECT * from account_order_info'
    return sqlite.select_all(sql)


def select_by_user_id(user_id):
    sql = 'SELECT * from account_order_info WHERE user_id = ?'
    return sqlite.select_by_key(user_id, sql)


def delete_all():
    sql = 'DELETE from account_order_info'
    sqlite.delete_all(sql)


def delete_by_user_id(user_id):
    sql = 'DELETE FROM account_order_info WHERE user_id = ?'
    sqlite.delete_by_key(user_id, sql)

