import sqlite3
import os
from typing import List


class DbConnection(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DbConnection, cls).__new__(cls)
        return cls.instance

    ddlCatalog = './ddl'
    conn = sqlite3.connect('etl.db')
    cursor = conn.cursor()

    def commit(self):
        self.conn.commit()

    def initializeClients(self):
        self.initializeTable('clients-ddl.sql')

    def initializeAccounts(self):
        self.initializeTable('accounts-ddl.sql')

    def initializeCards(self):
        self.initializeTable('cards-ddl.sql')

    def initializePassportBlacklist(self):
        self.initializeTable('passports-blacklist-ddl.sql')

    def initializeTerminals(self):
        self.initializeTable('terminals-ddl.sql')

    def initializeTransactions(self):
        self.initializeTable('transactions-ddl.sql')

    def initialize_all(self):
        print('Инициализация БД')
        self.initializeClients()
        self.initializeAccounts()
        self.initializeCards()
        self.initializePassportBlacklist()
        self.initializeTerminals()
        self.initializeTransactions()

    def initializeTable(self, ddlFilename):
        with open(self.ddlCatalog + '/' + ddlFilename) as file:
            sql = file.read()
            statements: List[str] = sql.split(';')
            for s in statements:
                if len(s) > 0:
                    self.cursor.execute(s)

    def check_existence(self, query, params):
        self.cursor.execute(query, params)
        data = self.cursor.fetchone()
        return data is not None
