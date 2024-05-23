drop table mytab cascade;

create tag table if not exists mytab (name varchar(32) primary key, time datetime basetime, value double summarized);

delete from mytab;

select * from v$mytab_stat;

select * from mytab limit 100;

backup table mytab into disk='/tmp/mytab1';

BACKUP TABLE mytab FROM TO_DATE('2023-01-01 00:00:00','YYYY-MM-DD HH24:MI:SS')
                         TO TO_DATE('2023-01-31 23:59:59','YYYY-MM-DD HH24:MI:SS')
                         INTO DISK = '/tmp/mytab-time1';


MOUNT database '/tmp/mytab1' to mnt1;

MOUNT database '/tmp/mytab-time1' to mnt2;
