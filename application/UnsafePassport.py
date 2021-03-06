import datetime

from application.DefaultRepository import DefaultRepository


class UnsafePassport:
    number = ''
    date = datetime.date.min


class UnsafePassportRepository:
    @staticmethod
    def passport_already_exists(passport_id):
        return DefaultRepository() \
            .check_existence('''SELECT * FROM [DE5.tkrv_DWH_FACT_passport_blacklist] AS bp WHERE bp.passport_num = ? '''
                             , [passport_id])

    @staticmethod
    def insert_unsafe_passport(entry: UnsafePassport):
        query = '''
           INSERT INTO [DE5.tkrv_DWH_FACT_passport_blacklist]
           (passport_num
           , entry_dt)
           VALUES(?,?); 
           '''
        executor = DefaultRepository().cursor
        executor.execute(query,
                         [entry.number, entry.date])
        DefaultRepository().commit()
