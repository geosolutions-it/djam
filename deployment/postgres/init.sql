
SELECT 'CREATE DATABASE djam'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'djam')\gexec
CREATE USER djam SUPERUSER;
ALTER USER djam CREATEDB;
ALTER USER djam WITH PASSWORD 'djam';
