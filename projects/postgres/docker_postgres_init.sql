/* We use this file to create a separate db, for airflow, so that we can have all neatly spinup */
CREATE USER admin WITH PASSWORD 'admin' CREATEDB;
CREATE DATABASE airflow
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
