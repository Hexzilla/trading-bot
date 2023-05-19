from db import sqlite


def insert_account(account):
    sql = ''' INSERT INTO account_info (user_id, enabled_user) VALUES(?,?) '''
    return sqlite.insert(account, sql)


def update_account(account):
    account_id = account[0]
    sql = '''UPDATE account_info SET user_id = ?, enabled_user = ? WHERE user_id = ?'''
    sqlite.update((*account, account_id), sql)


def upsert_account(account):
    exists = select_by_user_id(account[0])
    if not exists:
        insert_account(account)
    else:
        update_account(account)


def select_all():
    sql = 'SELECT * from account_info'
    return sqlite.select_all(sql)


def select_by_user_id(user_id):
    sql = 'SELECT * from account_info WHERE user_id = ?'
    return sqlite.select_by_key(user_id, sql)


def select_by_enabled_user(enabled_user):
    sql = 'SELECT * from account_info WHERE enabled_user = ?'
    return sqlite.select_by_key(enabled_user, sql)


def delete_all():
    sql = 'DELETE from account_info'
    sqlite.delete_all(sql)


def delete_by_user_id(user_id):
    sql = 'DELETE FROM account_info WHERE user_id = ?'
    sqlite.delete_by_key(user_id, sql)


def delete_by_enabled_user(enabled_user):
    sql = 'DELETE FROM account_info WHERE enabled_user = ?'
    sqlite.delete_by_key(enabled_user, sql)
