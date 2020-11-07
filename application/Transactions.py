import datetime
from decimal import *

from application.DbConnection import DbConnection


class Transaction:
    id = ''
    date = datetime.datetime.min
    card_number = ''
    operation_type = ''
    amount = Decimal(0)
    operation_result = ''
    terminal_id = ''


class TransactionRepository:
    @staticmethod
    def transaction_already_exists(transaction_id):
        return DbConnection() \
            .check_existence('''SELECT * FROM [DE5.tkrv_DWH_FACT_transactions] AS tr WHERE tr.trans_id = ? '''
                             , [transaction_id])

    @staticmethod
    def insert_transaction(entry: Transaction):
        query = '''
        INSERT INTO [DE5.tkrv_DWH_FACT_transactions]
        (trans_id
        , trans_date
        , card_num
        , oper_type
        , amt
        , oper_result
        , terminal)
        VALUES(?,?,?,?,?,?,?); 
        '''
        executor = DbConnection().cursor
        executor.execute(query,
                         [entry.id, entry.date, entry.card_number, entry.operation_type, entry.amount, entry.operation_result, entry.terminal_id])
        DbConnection().commit()
