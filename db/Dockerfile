FROM mysql:8.0.39


ENV MYSQL_DATABASE=my_house \
    MYSQL_ROOT_PASSWORD=admin
USER root
ENV MYSQL_ROOT_PASSWORD="admin"
COPY /data.sql /docker-entrypoint-initdb.d


EXPOSE 3307