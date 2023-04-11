from db import sqlite


def insert_auth(auth):
    sql = ''' INSERT INTO auths (api_key, oauth_state, expiration_date) VALUES(?,?,?) '''
    return sqlite.insert(auth, sql)


def update_auth(auth):
    sql = '''UPDATE auths 
             SET api_key = ?, 
                 oauth_state = ?, 
                 expiration_date = ?
             WHERE api_key = ?'''
    sqlite.update(auth, sql)


def select_all():
    sql = 'SELECT * from auths'
    return sqlite.select_all(sql)


def select_by_api_key(api_key):
    sql = 'SELECT * from auths WHERE api_key = ?'
    return sqlite.select_by_key(api_key, sql)


def select_by_oauth_state(oauth_state):
    sql = 'SELECT * from auths WHERE oauth_state = ?'
    return sqlite.select_by_key(oauth_state, sql)


def delete_all():
    sql = 'DELETE from auths'
    sqlite.delete_all(sql)


def delete_by_api_key(api_key):
    sql = 'DELETE FROM auths WHERE api_key = ?'
    sqlite.delete_by_key(api_key, sql)


def delete_by_oauth_state(oauth_state):
    sql = 'DELETE FROM auths WHERE oauth_state = ?'
    sqlite.delete_by_key(oauth_state, sql)
