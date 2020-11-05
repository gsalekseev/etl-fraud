import datetime
from decimal import *


class Transaction:
    id = ''
    date = datetime.date.min
    cardNumber = ''
    operationType = ''
    amount = Decimal(0)
    operationResult = ''
    terminalId = ''
