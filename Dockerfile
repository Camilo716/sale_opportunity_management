# TOMADO DE: https://hg.tryton.org/tryton-docker/file/tip/6.6/Dockerfile
FROM node as builder-node

ENV SERIES 6.8
RUN npm install -g bower
RUN curl https://downloads.tryton.org/${SERIES}/tryton-sao-6.8.4.tgz | tar zxf - -C /
RUN cd /package && bower install --allow-root

FROM python:3.9-bullseye

# trytond DB_CACHE requiere commandos `pg_dump` y `pg_restore`
RUN apt-get update && apt-get install -y postgresql-client

# TOMADO DE: https://hg.tryton.org/tryton-docker/file/tip/6.6/Dockerfile
COPY --from=builder-node /package /var/lib/trytond/www

