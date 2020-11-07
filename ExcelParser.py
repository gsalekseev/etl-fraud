import datetime
import xlrd
import os

from Account import Account, AccountRepository
from Card import Card, CardRepository
from Client import Client, ClientRepository
from Terminal import Terminal, TerminalRepository
from Transactions import Transaction, TransactionRepository
from UnsafePassport import UnsafePassport, UnsafePassportRepository


def fill_transactions():
    print('Заполнение БД транзакциями из файлов НАЧАТО')
    transaction_files = list(filter(lambda f: 'transactions' in f and 'backup' not in f, os.listdir(".")))
    transaction_files.sort(reverse=True)
    print('Найдено файлов для загрузки: ' + str(len(transaction_files)))
    # загрузка всех файлов транзакций, начиная с последнего, т.к. транзакции накапливаются
    for f in transaction_files:
        load_transactions_file(f)
    print('Заполнение БД транзакциями из файлов ЗАКОНЧЕНО')


def fill_passport_blacklist():
    print('Заполнение БД паспортами из черного списка НАЧАТО')
    blacklist_files = list(filter(lambda f: 'passports_blacklist' in f and 'backup' not in f, os.listdir(".")))
    print('Найдено файлов для загрузки: ' + str(len(blacklist_files)))
    for f in blacklist_files:
        load_passport_file(f)
    print('Заполнение БД паспортами из черного списка ЗАКОНЧЕНО')


def load_passport_file(filename):
    print('загрузка файла недействительных паспортов ' + filename + ' НАЧАТА')
    location = ('./' + filename)
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)
    row_num = sheet.nrows - 1
    #на первой строке шапка, поэтому до 1 строки включительно
    while row_num > 0:
        # добавление именно в таком порядке, чтобы сохранить целостность вторичных ключей
        handle_passport(row_num, sheet)
        row_num = row_num - 1
    print('загрузка файла недействительных паспортов ' + filename + ' ЗАВЕРШЕНА')
    #os.rename(location, location + '.backup')


def handle_passport(row_num, sheet):
    unsafe_passport = UnsafePassport()
    unsafe_passport.number = str(sheet.cell_value(row_num, 0)).split('.')[0]
    date = sheet.cell_value(row_num, 1)
    unsafe_passport.date = xlrd.xldate.xldate_as_datetime(date, 0)
    if not UnsafePassportRepository.passport_already_exists(unsafe_passport.number):
        UnsafePassportRepository.insert_unsafe_passport(unsafe_passport)


def load_transactions_file(filename):
    print('загрузка файла транзакций ' + filename + ' НАЧАТА')
    location = ('./' + filename)
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)
    row_num = sheet.nrows - 1
    print(row_num)
    # на первой строке шапка, поэтому до 1 строки включительно
    while row_num > 0:
        # добавление именно в таком порядке, чтобы сохранить целостность вторичных ключей
        handle_client(row_num, sheet)
        handle_account(row_num, sheet)
        handle_card(row_num, sheet)
        handle_terminal(row_num, sheet)
        handle_transaction(row_num, sheet)
        row_num = row_num - 1
    print('загрузка файла транзакций ' + filename + ' ЗАВЕРШЕНА')
    #os.rename(location, location + '.backup')


def handle_client(row_num, sheet):
    client = Client()
    client.client_id = sheet.cell_value(row_num, 5)
    client.last_name = sheet.cell_value(row_num, 6)
    client.first_name = sheet.cell_value(row_num, 7)
    client.patrinymic = sheet.cell_value(row_num, 8)
    print(sheet.cell_value(row_num, 9))
    date = int(sheet.cell_value(row_num, 9))
    client.date_of_birth = xlrd.xldate.xldate_as_datetime(date, 0)
    client.created = datetime.datetime.now()
    client.updated = datetime.datetime.now()
    if not ClientRepository.client_already_exists(client.client_id):
        ClientRepository.insert_client(client)


def handle_account(row_num, sheet):
    account = Account()
    account.account_number = sheet.cell_value(row_num, 3)
    date = sheet.cell_value(row_num, 4)
    account.valid_to = xlrd.xldate.xldate_as_datetime(date, 0)
    account.client_id = sheet.cell_value(row_num, 5)
    account.created = datetime.datetime.now()
    account.updated = datetime.datetime.now()
    if not AccountRepository.account_already_exists(account.account_number):
        AccountRepository.insert_account(account)


def handle_card(row_num, sheet):
    card = Card()
    card.card_number = sheet.cell_value(row_num, 2)
    card.account_number = sheet.cell_value(row_num, 3)
    card.created = datetime.datetime.now()
    card.updated = datetime.datetime.now()
    if not CardRepository.card_already_exists(card.card_number):
        CardRepository.insert_card(card)


def handle_terminal(row_num, sheet):
    terminal = Terminal()
    terminal.terminal_id = sheet.cell_value(row_num, 16)
    terminal.type = sheet.cell_value(row_num, 17)
    terminal.city = sheet.cell_value(row_num, 18)
    terminal.address = sheet.cell_value(row_num, 18)
    terminal.created = datetime.datetime.now()
    terminal.updated = datetime.datetime.now()
    if not TerminalRepository.terminal_already_exists(terminal.terminal_id):
        TerminalRepository.insert_terminal(terminal)


def handle_transaction(row_num, sheet):
    transaction = Transaction()
    transaction.id = str(sheet.cell_value(row_num, 0)).split('.')[0]
    date = sheet.cell_value(row_num, 1)
    transaction.date = xlrd.xldate.xldate_as_datetime(date, 0)
    transaction.card_number = sheet.cell_value(row_num, 2)
    transaction.operation_type = sheet.cell_value(row_num, 13)
    transaction.operation_result = sheet.cell_value(row_num, 15)
    transaction.amount = sheet.cell_value(row_num, 14)
    transaction.terminal_id = sheet.cell_value(row_num, 16)
    transaction.created = datetime.datetime.now()
    transaction.updated = datetime.datetime.now()
    if not TransactionRepository.transaction_already_exists(transaction.id):
        TransactionRepository.insert_transaction(transaction)
