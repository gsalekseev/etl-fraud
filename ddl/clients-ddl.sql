DROP TABLE IF EXISTS [DE5.tkrv_DWH_DIM_clients];

CREATE TABLE [DE5.tkrv_DWH_DIM_clients] (
    client_id         VARCHAR  PRIMARY KEY,
    first_name        VARCHAR,
    last_name         VARCHAR,
    patrinymic        VARCHAR,
    date_of_birth     DATE,
    passport_num      VARCHAR,
    passport_valid_to DATE,
    phone             VARCHAR,
    create_dt         DATETIME DEFAULT (CURRENT_TIMESTAMP),
    update_dt         DATETIME DEFAULT (CURRENT_TIMESTAMP)
);
