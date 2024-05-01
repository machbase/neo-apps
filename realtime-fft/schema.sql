create tag table tag (name varchar(32) primary key, time datetime basetime, value double summarized);

select count(*) from tag;

delete from tag;


create log table alarm (name varchar(32), time datetime, value double);

select * from alarm;

delete from alarm;




