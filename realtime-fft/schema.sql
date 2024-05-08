drop table fft cascade;

create tag table if not exists fft (name varchar(32) primary key, time datetime basetime, value double summarized);

select count(*) from fft;

delete from fft;

CREATE RETENTION policy_1m_1d DURATION 1 MONTH INTERVAL 1 DAY;
ALTER TABLE fft ADD RETENTION policy_1m_1d;
SELECT * FROM V$RETENTION_JOB;