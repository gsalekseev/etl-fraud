import datetime

from application.DefaultRepository import DefaultRepository


class Client:
    client_id = ''
    first_name = ''
    last_name = ''
    patrinymic = ''
    date_of_birth = datetime.date.min
    passport_num = ''
    passport_valid_to = datetime.date.min
    phone = ''
    created = datetime.date.min
    updated = datetime.date.min


class ClientRepository:
    @staticmethod
    def client_already_exists(client_id):
        return DefaultRepository() \
            .check_existence('''SELECT * FROM [DE5.tkrv_DWH_DIM_clients] AS cl WHERE cl.client_id = ? '''
                             , [client_id])

    @staticmethod
    def insert_client(entry: Client):
        query = '''
        INSERT INTO [DE5.tkrv_DWH_DIM_clients] 
        (client_id
        , first_name
        , last_name
        , patrinymic
        , date_of_birth
        , passport_num
        , passport_valid_to
        , phone
        , create_dt
        , update_dt)
        VALUES(?,?,?,?,?,?,?,?,?,?); 
        '''
        executor = DefaultRepository().cursor
        executor.execute(query,
                         [entry.client_id, entry.first_name, entry.last_name, entry.patrinymic, entry.date_of_birth,
                          entry.passport_num, entry.passport_valid_to, entry.phone, entry.created, entry.updated])
        DefaultRepository().commit()
