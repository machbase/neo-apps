
create tag table if not exists monitoring (
    name varchar(128) primary key,
    time datetime basetime,
    value double summarized
) with rollup;

