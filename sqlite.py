#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import time
import sqlite3
import traceback
from logger import logger


class Sqlite:
    def __init__(self):
        self.database_path = 'test.db'
        self.table_name = 'test'

        self.conn = None
        self.cursor = None

        self.connect()
        self.initialize()

    def connect(self):
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()

    def initialize(self):
        sql = "CREATE TABLE IF NOT EXISTS {} (" \
              "id VARCHAR(20) PRIMARY KEY NOT NULL," \
              "name VARCHAR(200) NOT NULL," \
              "jmeter TEXT," \
              "application TEXT," \
              "database TEXT," \
              "others TEXT," \
              "is_valid INTEGER default 1," \
              "sort INTEGER);".format(self.table_name)
        self.cursor.execute(sql)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


database_path = 'test.db'
table_name = 'test'

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

sql = "CREATE TABLE IF NOT EXISTS {} (" \
      "id VARCHAR(20) PRIMARY KEY NOT NULL," \
      "name VARCHAR(200) NOT NULL," \
      "jmeter TEXT," \
      "application TEXT," \
      "database TEXT," \
      "others TEXT," \
      "is_valid INTEGER default 1," \
      "sort INTEGER);".format(table_name)
cursor.execute(sql)
conn.commit()


class Executor:
    def __init__(self):
        self.insert_sql = "INSERT INTO {} VALUES {};"
        self.select_sql = "SELECT * FROM {} ORDER BY SORT;"
        self.update_sql = "UPDATE {} SET {} WHERE id = {};"
        self.delete_sql = "DELETE FROM {} WHERE id = {};"
        self.edit_sql = "SELECT * FROM {} WHERE id = {};"
        self.max_sort_sql = "SELECT SORT FROM {} ORDER BY SORT DESC LIMIT 1;"
        self.current_sort_sql = "SELECT SORT FROM {} WHERE id = {};"

        self.sqlite = Sqlite()

    def show(self):
        self.sqlite.cursor.execute(self.select_sql.format(self.sqlite.table_name))
        data = self.sqlite.cursor.fetchall()
        return data

    def is_valid(self, data):
        Id = data.get('Id')
        is_valid = data.get('is_valid')
        field = 'is_valid = {}'.format(is_valid)
        self.sqlite.cursor.execute(self.update_sql.format(self.sqlite.table_name, field, Id))
        self.sqlite.conn.commit()

    def delete(self, Id):
        self.sqlite.cursor.execute(self.delete_sql.format(self.sqlite.table_name, Id))
        self.sqlite.conn.commit()

    def edit(self, Id):
        self.sqlite.cursor.execute(self.edit_sql.format(self.sqlite.table_name, Id))
        data = self.sqlite.cursor.fetchall()
        return data[0]

    def save(self, data):
        logger.info('save')
        name = data.get('name')
        jmeter = data.get('jmeter')
        application = data.get('application')
        database = data.get('database')
        others = data.get('others')
        is_valid = 1
        sort = self.max_sort() + 1

        values = (int(time.time() * 1000), name, jmeter, application, database, others, is_valid, sort)
        self.sqlite.cursor.execute(self.insert_sql.format(self.sqlite.table_name, values))
        self.sqlite.conn.commit()


    def max_sort(self):
        cursor = conn.cursor()
        cursor.execute(self.max_sort_sql.format(table_name))
        data = cursor.fetchall()
        return data[0]
        # self.sqlite.cursor.execute(self.max_sort_sql.format(self.sqlite.table_name))
        # data = self.sqlite.cursor.fetchall()
        # return data[0]

    def update(self, data):
        Id = data.get('Id')
        name = data.get('name')
        jmeter = data.get('jmeter')
        application = data.get('application')
        database = data.get('database')
        others = data.get('others')

        update_data = "name = {}, jmeter = {}, application = {}, database = {}, others = {}".format(name, jmeter, application, database, others)
        self.sqlite.cursor.execute(self.update_sql.format(self.sqlite.table_name, update_data, Id))
        self.sqlite.conn.commit()

    def move_up_down(self, Id, is_up = 0):
        self.sqlite.cursor.execute(self.current_sort_sql.format(self.sqlite.table_name, Id))
        current_sort = self.sqlite.cursor.fetchall()[0]

        if is_up == 0:
            try:
                downer_sql = "SELECT id FROM {} WHERE SORT > {} ORDER BY SORT LIMIT 1;".format(self.sqlite.table_name, current_sort)
                self.sqlite.cursor.execute(downer_sql)
                move_id = self.sqlite.cursor.fetchall()[0]

                update_data = "sort = {}".format(current_sort + 1)
                update_data1 = "sort = {}".format(current_sort)
                self.sqlite.cursor.execute(self.update_sql.format(self.sqlite.table_name, update_data, Id))
                self.sqlite.cursor.execute(self.update_sql.format(self.sqlite.table_name, update_data1, move_id))
                self.sqlite.conn.commit()
            except IndexError:
                logger.error(traceback.format_exc())
                raise Exception('Is is up to the last one!')

        elif is_up == 1:
            try:
                downer_sql = "SELECT id FROM {} WHERE SORT < {} ORDER BY SORT DESC LIMIT 1;".format(self.sqlite.table_name, current_sort)
                self.sqlite.cursor.execute(downer_sql)
                move_id = self.sqlite.cursor.fetchall()[0]

                update_data = "sort = {}".format(current_sort - 1)
                update_data1 = "sort = {}".format(current_sort)
                self.sqlite.cursor.execute(self.update_sql.format(self.sqlite.table_name, update_data, Id))
                self.sqlite.cursor.execute(self.update_sql.format(self.sqlite.table_name, update_data1, move_id))
                self.sqlite.conn.commit()
            except IndexError:
                logger.error(traceback.format_exc())
                raise Exception('It is up to the first one!')

    def __del__(self):
        del self.sqlite
