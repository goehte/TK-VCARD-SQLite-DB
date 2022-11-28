# -*- coding: utf-8 -*-
# https://www.sqlitetutorial.net/sqlite-python/creating-database/
# app/db.py

"""This module provides a database connection."""

from datetime import datetime
import sqlite3
from sqlite3 import Error


def create_db_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_file = r"app/app.db"
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #db_status = (f"Connect SQL DB {db_file} V{sqlite3.version}")
    except Error as e:
        print(f"SQL Error: {e}")
    return conn

def close_db_connection(conn):
    """close database connection """
    if conn is not None:
      conn.close()
    else:
        print("Error! cannot close the database connection.")
      
def read_db_table(order):
    """ read a table with sql statement
    :param conn: Connection object
    :return: Data rows
    """
    if order == "" : order = "ID"
    sql = ''' SELECT ID, N_FIRST, N_LAST, ORG, EMAIL, TITLE, ROLE, CATEGORIES FROM vcard'''
    sql += (" ORDER BY " + order)
    try:
      conn = create_db_connection()
      c = conn.cursor()
      c.execute(sql)
      rows = c.fetchall()
      close_db_connection(conn)
      return rows
    except Error as e:
      print(f"SQL Error: {e}")


def search_db_table(search_query):
    """ read a table with sql statement
    :param conn: Connection object
    :return: Data rows
    """
    sql = ''' SELECT ID, N_FIRST, N_LAST, ORG, EMAIL, TITLE, ROLE, CATEGORIES FROM vcard 
    WHERE N_FIRST LIKE ?
    OR N_LAST LIKE ? 
    OR ORG LIKE ? 
    OR TITLE LIKE ? 
    OR ROLE LIKE ? 
    OR CATEGORIES LIKE ? '''
    search_query = "%"+search_query+"%"
    try:
      conn = create_db_connection()
      c = conn.cursor()
      c.execute(sql, (search_query, search_query, search_query, search_query, search_query, search_query)) 
    # each "?" of a SQL Query gets an argument, see: https://www.sqlitetutorial.net/sqlite-python/update/
      rows = c.fetchall()
      close_db_connection(conn)
      #print(f"Serach: {search_query}")
      return rows
    except Error as e:
      print(f"SQL Error: {e}")
    
def read_single_db_table_enty(id):
    """ read a table with sql statement
    :param conn: Connection object
    :return: Signle data row
    """
    sql = ''' SELECT ID, N_FIRST, N_LAST, ORG, EMAIL, URL, TEL_WORK_CELL, TEL_WORK_VOICE, TEL_HOME_CELL, TEL_HOME_VOICE, TITLE, ROLE, CATEGORIES, NOTE FROM vcard WHERE id = ? '''
    try:
      conn = create_db_connection()
      c = conn.cursor()
      c.execute(sql, (id,))
      row = c.fetchall()
      # Replace None Values with empty string:
      row = [tuple(s if s != None else '' for s in tup) for tup in row]

      close_db_connection(conn)
      return row
    except Error as e:
      print(f"SQL Error: {e}")

    

def add_db_entry(f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes):
    sql = ''' INSERT INTO vcard (ID, N_FIRST, N_LAST, ORG, EMAIL, URL, TEL_WORK_CELL, TEL_WORK_VOICE, TEL_HOME_CELL, TEL_HOME_VOICE, TITLE, ROLE, CATEGORIES, NOTE, REV) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    try:
      conn = create_db_connection()
      c = conn.cursor()
      c.execute(sql, (f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
      conn.commit()
      close_db_connection(conn)
      #print(f"Add {f_name}, {l_name}")
    except Error as e:
      print(f"SQL Error: {e}")


def update_db_entry(id, f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes):
    sql = ''' UPDATE vcard SET 
    N_FIRST = ?,
    N_LAST = ?,
    ORG = ?,
    EMAIL = ?,
    URL = ?,
    TEL_WORK_CELL = ?,
    TEL_WORK_VOICE = ?,
    TEL_HOME_CELL = ?,
    TEL_HOME_VOICE = ?,
    TITLE = ?,
    ROLE = ?,
    CATEGORIES = ?,
    NOTE = ?,
    REV = ?
    WHERE id = ? '''
    try:
      conn = create_db_connection()
      c = conn.cursor()
      c.execute(sql, (f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id))
      conn.commit()
      close_db_connection(conn)
      #print(f"Update {id}, {f_name}, {l_name}")
    except Error as e:
      print(f"SQL Error: {e}")


def delete_db_entry(id):
    sql = ''' DELETE FROM vcard WHERE id = ? '''
    try:
      conn = create_db_connection()
      c = conn.cursor()
      c.execute(sql, (id,))
      conn.commit()
      close_db_connection(conn)
      #print(f"Delete: {id}")
    except Error as e:
      print(f"SQL Error: {e}")
