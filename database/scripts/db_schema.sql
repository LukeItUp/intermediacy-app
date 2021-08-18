
CREATE TABLE paper ( 
	id      serial  NOT NULL,
	ms_id   bigint,
    doi     varchar(200),        
    title   varchar(1000),
    authors varchar(2000),
    year    integer,
    fields  varchar(2000),

	CONSTRAINT pk_page_id PRIMARY KEY ( id )
 );