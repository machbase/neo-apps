drop table home cascade;

create tag table home (name varchar(32) primary key, time datetime basetime, value double summarized) with rollup;

select count(*) from home;

select min(time), max(time) from home;

