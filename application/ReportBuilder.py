import datetime

from application.DefaultRepository import DefaultRepository
from application.FraudReportEntry import FraudReportEntry


def build_report():
    print("Построение отчета НАЧАТО")
    set_unsafe_transactions()
    print("Построение отчета ЗАВЕРШЕНО. Инкремент данных сохранен")


def get_report():
    print("Вывод отчета на текущий момент НАЧАТ")
    connection = DefaultRepository()
    connection.cursor.execute('''SELECT * FROM [DE5.tkrv_REP_FRAUD]''')
    rows = connection.cursor.fetchall()
    for r in rows:
        print(r)
    print("Вывод отчета на текущий момент ЗАВЕРШЕН")


def set_unsafe_transactions():
    total_events = get_report_events()

    # устанавливаем дату отчета
    dt = datetime.datetime.now()
    for e in total_events:
        insert_event(e, dt)


def get_events(sql):
    connection = DefaultRepository()
    connection.cursor.execute(sql)
    rows = connection.cursor.fetchall()
    events = []
    for d in rows:
        event = FraudReportEntry()
        event.event_datetime = d[1]
        event.passport = d[2]
        event.fio = d[3]
        event.phone = d[4]
        event.event_type = d[5]
        events.append(event)
    return events


def insert_event(e: FraudReportEntry, datetime):
    connection = DefaultRepository()
    connection.cursor.execute('''INSERT INTO [DE5.tkrv_REP_FRAUD] (
                                     event_dt,
                                     passport,
                                     fio,
                                     phone,
                                     event_type,
                                     report_dt
                                 )
                                 VALUES (
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                     ?
                                 );''', [e.event_datetime, e.passport, e.fio, e.phone, e.event_type, datetime])
    connection.commit()


def get_report_events():
    return get_events('''SELECT * FROM (
SELECT inrrpt.RN, inrrpt.trans_date, inrrpt.passport_num, inrrpt.fio, inrrpt.phone, inrrpt.event_type
, ROW_NUMBER() OVER (PARTITION BY inrrpt.passport_num ORDER BY inrrpt.trans_date DESC) AS ROW_NUM
FROM
(

SELECT * FROM (
SELECT DISTINCT
ROW_NUMBER() OVER (PARTITION BY cl.passport_num ORDER BY tr.trans_date DESC) AS RN
, tr.trans_date
, cl.passport_num
, cl.last_name || ' ' || cl.first_name || ' ' || cl.patrinymic AS fio
, cl.phone
, 'Паспорт в черном списке' AS event_type
  FROM [DE5.tkrv_DWH_FACT_transactions] AS tr
  INNER JOIN [DE5.tkrv_DWH_DIM_cards] AS crd
      ON crd.card_num = tr.card_num
  INNER JOIN  [DE5.tkrv_DWH_DIM_accounts] AS acc
      ON acc.account_num = crd.account_num
  INNER JOIN [DE5.tkrv_DWH_DIM_clients] AS cl
      ON cl.client_id = acc.client
  INNER JOIN [DE5.tkrv_DWH_FACT_passport_blacklist] AS pssprt
      ON pssprt.passport_num = cl.passport_num)
  WHERE RN  = 1
UNION ALL
--просроченные паспорта
SELECT * FROM
(
    SELECT DISTINCT
    ROW_NUMBER() OVER (PARTITION BY cl.passport_num ORDER BY tr.trans_date DESC) AS RN
    , tr.trans_date
    , cl.passport_num
    , cl.last_name || ' ' || cl.first_name || ' ' || cl.patrinymic AS fio
    ,cl.phone
    , 'Просрочен паспорт' AS event_type
    FROM [DE5.tkrv_DWH_FACT_transactions] AS tr
    INNER JOIN [DE5.tkrv_DWH_DIM_cards] AS crd
          ON crd.card_num = tr.card_num
    INNER JOIN  [DE5.tkrv_DWH_DIM_accounts] AS acc
          ON acc.account_num = crd.account_num
    INNER JOIN [DE5.tkrv_DWH_DIM_clients] AS cl
          ON cl.client_id = acc.client
    WHERE cl.passport_valid_to < DATE('now')
) AS ev
WHERE ev.RN = 1
UNION ALL
--неактивные договора
SELECT * FROM
(
    SELECT
    ROW_NUMBER() OVER (PARTITION BY cl.passport_num ORDER BY tr.trans_date DESC) AS RN
    , tr.trans_date
    , cl.passport_num
    , cl.last_name || ' ' || cl.first_name || ' ' || cl.patrinymic AS fio
    ,cl.phone
    , 'Просрочен договор' AS event_type
    FROM [DE5.tkrv_DWH_FACT_transactions] AS tr
    INNER JOIN [DE5.tkrv_DWH_DIM_cards] AS crd
          ON crd.card_num = tr.card_num
    INNER JOIN  [DE5.tkrv_DWH_DIM_accounts] AS acc
          ON acc.account_num = crd.account_num
    INNER JOIN [DE5.tkrv_DWH_DIM_clients] AS cl
          ON cl.client_id = acc.client
    WHERE acc.valid_to < DATE('now')
) AS ev
WHERE ev.RN = 1
UNION ALL
SELECT * FROM
(
SELECT DISTINCT
ROW_NUMBER() OVER (PARTITION BY cl.passport_num ORDER BY tr.trans_date DESC) AS RN
, tr.trans_date
, cl.passport_num
, cl.last_name || ' ' || cl.first_name || ' ' || cl.patrinymic AS fio
,cl.phone
, 'Операции в разных городах в течение часа' AS event_type
  FROM [DE5.tkrv_DWH_FACT_transactions] AS tr
  INNER JOIN [DE5.tkrv_DWH_DIM_cards] AS crd
      ON crd.card_num = tr.card_num
  INNER JOIN  [DE5.tkrv_DWH_DIM_accounts] AS acc
      ON acc.account_num = crd.account_num
  INNER JOIN [DE5.tkrv_DWH_DIM_clients] AS cl
      ON cl.client_id = acc.client
  INNER JOIN [DE5.tkrv_DWH_DIM_terminals] AS trml /* терминал первой транзакции */
      ON trml.terminal_id = tr.terminal
  INNER JOIN [DE5.tkrv_DWH_FACT_transactions] AS tr2 /* ищем транзакцию, которая была в другом городе. вторая транзакция  */
      ON tr2.card_num = tr.card_num /* транзакции по одной карте */
      AND tr2.terminal <> tr.terminal /* транзакции на разных терминалах */
      AND ABS(CAST ((JULIANDAY(tr.trans_date) - JULIANDAY(tr2.trans_date)) * 24 AS INTEGER)) < 1 /* модуль разницы транзакций в часах */
  INNER JOIN [DE5.tkrv_DWH_DIM_terminals] AS trml2 /* терминал второй транзакции */
      ON trml2.terminal_id = tr2.terminal
  WHERE trml2.terminal_city <> trml.terminal_city
    ) AS ev
WHERE ev.RN = 1
UNION ALL
SELECT * FROM
(
    SELECT DISTINCT
    ROW_NUMBER() OVER (PARTITION BY cl.passport_num ORDER BY tr.trans_date DESC) AS RN
    , tr.trans_date
    , cl.passport_num
    , cl.last_name || ' ' || cl.first_name || ' ' || cl.patrinymic AS fio
    ,cl.phone
    , 'Подбор суммы' AS event_type
    FROM [DE5.tkrv_DWH_FACT_transactions] AS tr
    INNER JOIN [DE5.tkrv_DWH_DIM_cards] AS crd
          ON crd.card_num = tr.card_num
    INNER JOIN  [DE5.tkrv_DWH_DIM_accounts] AS acc
          ON acc.account_num = crd.account_num
    INNER JOIN [DE5.tkrv_DWH_DIM_clients] AS cl
          ON cl.client_id = acc.client
    WHERE tr.trans_id IN 
               (
                  SELECT DISTINCT trans_id FROM 
                  (
                     SELECT innertr.*, COUNT(*) OVER(PARTITION BY innertr.card_num, innertr.amt) AS CNT
                     FROM [DE5.tkrv_DWH_FACT_transactions] AS innertr
                     INNER JOIN [DE5.tkrv_DWH_FACT_transactions] AS innertr2
                        ON innertr2.card_num = innertr.card_num
                     WHERE innertr.oper_result = 'Успешно' 
                     AND innertr2.oper_result = 'Отказ' 
                     AND ABS(CAST ((JULIANDAY(innertr2.trans_date) - JULIANDAY(innertr.trans_date)) * 24 * 60 AS INTEGER)) <= 20 /* разница в минутах не более 20 */
                    ) AS tr
                  WHERE tr.CNT >=3       
               )
) AS ev
WHERE ev.RN = 1
) AS inrrpt) WHERE ROW_NUM = 1
''')
