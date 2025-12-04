import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=(), return_lastrowid=False):
    con = get_connection()
    cur = con.execute(sql, params)
    con.commit()
    last_id = cur.lastrowid
    con.close()

    if return_lastrowid:
        return last_id

def query(sql, params=(), one=False):
    con = get_connection()
    cur = con.execute(sql, params)

    if one:
        row = cur.fetchone()
        con.close()
        return row

    rows = cur.fetchall()
    con.close()
    return rows


def get_comments(report_id):
    sql = "SELECT username, content, created_at FROM comments WHERE report_id = ? ORDER BY created_at DESC"
    return query(sql, [report_id])

def add_comment(report_id, username, content):
    sql = "INSERT INTO comments (report_id, username, content) VALUES (?, ?, ?)"
    execute(sql, [report_id, username, content])

