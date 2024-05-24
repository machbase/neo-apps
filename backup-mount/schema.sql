drop table mytab_A cascade;
drop table mytab_B cascade;

create tag table if not exists mytab_A (name varchar(32) primary key, time datetime basetime, value double summarized) tag_partition_count=1;
create tag table if not exists mytab_B (name varchar(32) primary key, time datetime basetime, value double summarized) tag_partition_count=1;;

delete from mytab_A;
delete from mytab_B;

-- online data check
select min(time), max(time) from mytab_A;
select count(*) from mytab_A;
select * from mytab_A limit 10;

select min(time), max(time) from mytab_B;
select count(*) from mytab_B;
select * from mytab_B limit 10;

-- 1. backup full database 

backup database  into disk='/tmp/mybkup1';

mount database '/tmp/mybkup1' to mountdb1;

select min(time), max(time) from mountdb1.sys.mytab_A;
select count(*) from mountdb1.sys.mytab_A;
select * from mountdb1.sys.mytab_A limit 10;


select min(time), max(time) from mountdb1.sys.mytab_B;
select count(*) from mountdb1.sys.mytab_B;
select * from mountdb1.sys.mytab_B limit 10;

umount database mountdb1;

-- 2. backup full database within time-range

backup database  FROM TO_DATE('2023-01-01 00:00:00','YYYY-MM-DD HH24:MI:SS')
                         TO TO_DATE('2023-01-31 23:59:59','YYYY-MM-DD HH24:MI:SS') into disk='/tmp/mybkup2';

delete from mytab_B before TO_DATE('2023-01-31 23:59:59','YYYY-MM-DD HH24:MI:SS');

select min(time), max(time) from mytab_B;

select * from mytab_b where time between TO_DATE('2023-01-01 00:00:00','YYYY-MM-DD HH24:MI:SS')
                         and TO_DATE('2023-01-31 23:59:59','YYYY-MM-DD HH24:MI:SS');

mount database '/tmp/mybkup2' to mountdb2;

select min(time), max(time) from mountdb2.sys.mytab_B;
select count(*) from mountdb2.sys.mytab_B;
select * from mountdb2.sys.mytab_B limit 10;

umount database mountdb2;

-- 3. backup table within time-range

BACKUP TABLE mytab_A FROM TO_DATE('2023-03-01 00:00:00','YYYY-MM-DD HH24:MI:SS')
                         TO TO_DATE('2023-03-31 23:59:59','YYYY-MM-DD HH24:MI:SS')
                         INTO DISK = '/tmp/mybkup3';

MOUNT database '/tmp/mybkup3' to mountdb3;

select min(time), max(time) from mountdb3.sys.mytab_A;
select count(*) from mountdb3.sys.mytab_A;
select * from mountdb3.sys.mytab_A limit 10;

umount database mountdb3;



