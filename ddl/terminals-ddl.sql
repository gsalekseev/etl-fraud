DROP TABLE IF EXISTS [DE5.tkrv_DWH_DIM_terminals];
CREATE TABLE [DE5.tkrv_DWH_DIM_terminals] (
    terminal_id      VARCHAR  PRIMARY KEY,
    terminal_type    VARCHAR,
    terminal_city    VARCHAR,
    terminal_address VARCHAR,
    create_dt        DATETIME DEFAULT (CURRENT_TIMESTAMP),
    update_dt         DATETIME DEFAULT (CURRENT_TIMESTAMP)
);
