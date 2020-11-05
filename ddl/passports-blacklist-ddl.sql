DROP TABLE IF EXISTS [DE5.tkrv_DWH_FACT_passport_blacklist];
CREATE TABLE [DE5.tkrv_DWH_FACT_passport_blacklist] (
    passport_num VARCHAR PRIMARY KEY
                         NOT NULL,
    entry_dt     DATE
);
