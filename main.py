from application.ExcelParser import fill_transactions, fill_passport_blacklist
from application.PackageHelper import install_package
from application.DbConnection import DbConnection

#признак использования чистой БД
clear_db = True

print('Установка пакета xlrd')
install_package("xlrd")

connection = DbConnection()

# проверяем БД на наличие таблиц
tables = connection.cursor.execute('''SELECT * FROM sqlite_master WHERE type='table';''')
if tables.fetchone() is None or clear_db:
    connection.initialize_all()
    connection.commit()

fill_transactions()
fill_passport_blacklist()

