import sqlite3
import os
from typing import List

# признак использования чистой БД каждый запуск
clear_db = False


class DefaultRepository(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DefaultRepository, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    ddlCatalog = './ddl'
    conn = sqlite3.connect('./etl.db')
    cursor = conn.cursor()

    def init(self):
        # проверяем БД на наличие таблиц
        tables = self.cursor.execute('''SELECT * FROM sqlite_master WHERE type='table';''')
        if tables.fetchone() is None or clear_db:
            self.initialize_all()
            self.commit()

    def commit(self):
        self.conn.commit()

    def initialize_clients(self):
        self.initialize_table('clients-ddl.sql')

    def initialize_accounts(self):
        self.initialize_table('accounts-ddl.sql')

    def initialize_cards(self):
        self.initialize_table('cards-ddl.sql')

    def initialize_passport_blacklist(self):
        self.initialize_table('passports-blacklist-ddl.sql')

    def initialize_terminals(self):
        self.initialize_table('terminals-ddl.sql')

    def initialize_transactions(self):
        self.initialize_table('transactions-ddl.sql')

    def initialize_report(self):
        self.initialize_table('fraud-report-ddl.sql')

    def initialize_all(self):
        print('Инициализация БД')
        self.initialize_clients()
        self.initialize_accounts()
        self.initialize_cards()
        self.initialize_passport_blacklist()
        self.initialize_terminals()
        self.initialize_transactions()
        self.initialize_report()

    def initialize_table(self, ddl_filename):
        with open(self.ddlCatalog + '/' + ddl_filename) as file:
            sql = file.read()
            statements: List[str] = sql.split(';')
            for s in statements:
                if len(s) > 0:
                    self.cursor.execute(s)

    def check_existence(self, query, params):
        self.cursor.execute(query, params)
        data = self.cursor.fetchone()
        return data is not None

    def run_query(self, sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
