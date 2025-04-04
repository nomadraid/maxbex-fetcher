/****  GET STARTED WITH YOUR TIMESCALE CLOUD SERVICE  ****/


/*
SERVICE INFORMATION:

Service name:  db_88795
Database name: tsdb
Username:      tsdbadmin
Password:      XXXXXXXXXXX
Service URL:   postgres://tsdbadmin:XXXXXXXXXXX@XXXXXXXXXXX.XXXXXXXXXXX.tsdb.cloud.timescale.com:34010/tsdb?sslmode=require
Port:          34010


~/.pg_service.conf
echo "
[db_88795]
host=XXXXXXXXXXX.XXXXXXXXXXX.tsdb.cloud.timescale.com
port=34010
user=tsdbadmin
password=XXXXXXXXXXX
dbname=tsdb
" >> ~/.pg_service.conf
psql -d "service=db_88795"
*/

----------------------------------------------------------------------------

/*
 ╔╗
╔╝║
╚╗║
 ║║         CONNECT TO YOUR SERVICE
╔╝╚╦╗
╚══╩╝

 ​
1. Install psql:
    https://blog.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/

2. From your command line, run:
    psql "postgres://tsdbadmin:XXXXXXXXXXX@XXXXXXXXXXX.XXXXXXXXXXX.tsdb.cloud.timescale.com:34010/tsdb?sslmode=require"
*/

----------------------------------------------------------------------------

/*
╔═══╗
║╔═╗║
╚╝╔╝║
╔═╝╔╝	    CREATE A HYPERTABLE
║ ╚═╦╗
╚═══╩╝
*/

CREATE TABLE conditions (	-- create a regular table
    time        TIMESTAMPTZ       NOT NULL,
    location    TEXT              NOT NULL,
    temperature DOUBLE PRECISION  NULL
);

SELECT create_hypertable('conditions', 'time');	-- turn it into a hypertable

----------------------------------------------------------------------------

/*
╔═══╗
║╔═╗║
╚╝╔╝║
╔╗╚╗║      INSERT DATA
║╚═╝╠╗
╚═══╩╝
*/

INSERT INTO conditions
  VALUES
    (NOW(), 'office', 70.0),
    (NOW(), 'basement', 66.5),
    (NOW(), 'garage', 77.0);
​
----------------------------------------------------------------------------

/*
FOR MORE DOCUMENTATION AND GUIDES, VISIT	>>>--->	HTTPS://DOCS.TIMESCALE.COM/
*/