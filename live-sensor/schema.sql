create tag table tag (name varchar(32) primary key, time datetime basetime, value double summarized);

select count(*) from tag;

delete from tag;

