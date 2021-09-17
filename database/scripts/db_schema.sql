
CREATE TABLE paper ( 
	id      serial  NOT NULL,
	ms_id   bigint,
    doi     varchar(200),        
    title   varchar(1000),
    authors varchar(2000),
    year    integer,
    fields  varchar(2000)
 );

 CREATE TABLE task (
     id         serial NOT NULL,
     task_id    varchar(8),
     task_name  varchar(100),
     file_path  varchar(100),
     source     varchar(100),
     target     varchar(100),
     status     varchar(10),
     results    varchar(2000)
 );