import datetime


class FraudReportEntry:
    event_datetime = datetime.datetime.min
    passport = ''
    fio = ''
    phone = ''
    event_type = ''
    report_dt = datetime.datetime.min