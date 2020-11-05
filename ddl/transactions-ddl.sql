DROP TABLE IF EXISTS [DE5.tkrv_DWH_FACT_transactions];
CREATE TABLE [DE5.tkrv_DWH_FACT_transactions] (
    trans_id    VARCHAR (100) CONSTRAINT PK_TRANSACTIONS PRIMARY KEY
                              UNIQUE,
    trans_date  DATE          NOT NULL
                              DEFAULT (CURRENT_TIMESTAMP),
    card_num    VARCHAR       CONSTRAINT FK_TRANSACTIONS_TO_CARDS REFERENCES [DE5.tkrv_DWH_DIM_cards] (card_num),
    oper_type   VARCHAR,
    amt         DECIMAL,
    oper_result VARCHAR,
    terminal    VARCHAR       CONSTRAINT FK_TRANSACTIONS_TO_TERMINALS REFERENCES [DE5.tkrv_DWH_DIM_terminals] (terminal_id)
);
