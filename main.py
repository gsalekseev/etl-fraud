from application.ExcelParser import fill_transactions, fill_passport_blacklist
from application.PackageHelper import install_package
from application.DefaultRepository import DefaultRepository

from application.ReportBuilder import build_report, get_report

print('Установка пакета xlrd')
install_package("xlrd")

connection = DefaultRepository()

new_trans_files_count = fill_transactions()
new_passports_files_count = fill_passport_blacklist()

# строим отчет на текущую дату, если были загрружены новые файлы
need_build_report = new_trans_files_count > 0 or new_passports_files_count > 0

if need_build_report:
    build_report()

get_report()
