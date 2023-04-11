import sqlite3
from sqlite3 import Error
from from_root import from_root, from_here

DB_FILE = str(from_root()) + '/db/sqlite3.db'


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql_script: str):
    try:
        c = conn.cursor()
        c.execute(create_table_sql_script)
    except Error as e:
        print(e)


def insert(data, sql_stmt: str):
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_stmt, data)
        conn.commit()

        return cur.lastrowid
    finally:
        if conn is not None:
            conn.close()


def update(data, sql_stmt: str):
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_stmt, data)
        conn.commit()
    finally:
        if conn is not None:
            conn.close()


def select_all(sql_stmt: str):
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_stmt)
        rows = cur.fetchall()

        return rows
    finally:
        if conn is not None:
            conn.close()


def select_by_key(key: str, sql_stmt: str):
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_stmt, (key,))
        rows = cur.fetchall()

        return rows
    finally:
        if conn is not None:
            conn.close()


def delete_all(sql_stmt: str):
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_stmt)
        conn.commit()
    finally:
        if conn is not None:
            conn.close()


def delete_by_key(key: str, sql_stmt: str):
    conn = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql_stmt, (key,))
        conn.commit()
    finally:
        if conn is not None:
            conn.close()