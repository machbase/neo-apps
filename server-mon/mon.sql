-- monitoring metric table 
create tag table if not exists monitoring (
    name varchar(128) primary key,
    time datetime basetime,
    value double summarized
) with rollup;

-- alarm history log table
create table alarm_history (name varchar(128), time datetime, value double, desc varchar(1024));
