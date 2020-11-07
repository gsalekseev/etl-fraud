import datetime

from application.DbConnection import DbConnection


class Terminal:
    terminal_id = ''
    type = ''
    city = ''
    address = ''
    created = datetime.date.min
    updated = datetime.date.min


class TerminalRepository:
    @staticmethod
    def terminal_already_exists(terminal_id):
        return DbConnection() \
            .check_existence('''SELECT * FROM [DE5.tkrv_DWH_DIM_terminals] AS tl WHERE tl.terminal_id = ? '''
                             , [terminal_id])

    @staticmethod
    def insert_terminal(entry: Terminal):
        query = '''
        INSERT INTO [DE5.tkrv_DWH_DIM_terminals]
        (terminal_id
        , terminal_type
        , terminal_city
        , terminal_address
        , create_dt
        , update_dt)
        VALUES(?,?,?,?,?,?); 
        '''
        executor = DbConnection().cursor
        executor.execute(query,
                         [entry.terminal_id, entry.type, entry.city, entry.address, entry.created, entry.updated])
        DbConnection().commit()
