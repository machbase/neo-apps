drop table fft cascade;

create tag table if not exists fft (name varchar(32) primary key, time datetime basetime, value double summarized);

select count(*) from fft;

delete from fft;




