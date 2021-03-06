DROP TABLE IF EXISTS [DE5.tkrv_DWH_DIM_accounts];

CREATE TABLE [DE5.tkrv_DWH_DIM_accounts] (
    account_num VARCHAR  PRIMARY KEY,
    valid_to    DATE,
    client      VARCHAR  CONSTRAINT FK_ACCOUNTS_TO_CLIENTS REFERENCES [DE5.tkrv_DWH_DIM_clients] (client_id),
    create_dt   DATETIME DEFAULT (CURRENT_TIMESTAMP),
    update_dt   DATETIME DEFAULT (CURRENT_TIMESTAMP)
);
