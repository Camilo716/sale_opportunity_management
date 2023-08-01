FROM python:3.9-bullseye

# trytond DB_CACHE requiere commandos `pg_dump` y `pg_restore`
RUN apt-get update && apt-get install -y postgresql-client
