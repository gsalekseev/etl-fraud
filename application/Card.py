import datetime

from application.DefaultRepository import DefaultRepository


class Card:
    card_number = ''
    account_number = ''
    created = datetime.date.min
    updated = datetime.date.min


class CardRepository:
    @staticmethod
    def card_already_exists(card_number):
        return DefaultRepository() \
            .check_existence('''SELECT * FROM [DE5.tkrv_DWH_DIM_cards] AS crd WHERE crd.card_num = ? '''
                             , [card_number])

    @staticmethod
    def insert_card(card: Card):
        query = '''
        INSERT INTO [DE5.tkrv_DWH_DIM_cards] (card_num, account_num, create_dt, update_dt)
        VALUES(?,?,?,?); 
        '''
        executor = DefaultRepository().cursor
        executor.execute(query, [card.card_number, card.account_number, card.created, card.updated])
        DefaultRepository().commit()
