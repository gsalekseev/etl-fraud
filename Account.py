import datetime

from DbConnection import DbConnection


class Account:
    account_number = ''
    valid_to = datetime.date.min
    client_id = ''
    created = datetime.date.min
    updated = datetime.date.min


class AccountRepository:
    @staticmethod
    def account_already_exists(account_number):
        return DbConnection() \
            .check_existence('''SELECT * FROM [DE5.tkrv_DWH_DIM_accounts] AS acc WHERE acc.account_num = ? '''
                             , [account_number])

    @staticmethod
    def insert_account(account: Account):
        query = '''
        INSERT INTO [DE5.tkrv_DWH_DIM_accounts] (account_num, valid_to, client, create_dt, update_dt)
        VALUES(?,?,?,?,?); 
        '''
        connection = DbConnection()
        executor = connection.cursor
        executor.execute(query, [account.account_number, account.valid_to, account.client_id, account.created,
                                 account.updated])
        connection.commit()
