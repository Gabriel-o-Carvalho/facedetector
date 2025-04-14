#!/bin/bash

# Configurações
CONTAINER_NAME="face_detector_db"
ROOT_PASSWORD="root"
DATABASE_NAME="controle_acesso_dee"
MYSQL_PORT=3306
SQL_SCRIPT="SQL Query.sql"

# Sobe o container
docker run --name $CONTAINER_NAME \
  -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD \
  -e MYSQL_DATABASE=$DATABASE_NAME \
  -p $MYSQL_PORT:3306 \
  -d mysql:latest  

# Espera o MySQL ficar pronto
echo "⏳ Aguardando o MySQL iniciar..."
until docker exec $CONTAINER_NAME mysqladmin ping -uroot -p$ROOT_PASSWORD --silent &> /dev/null; do
  sleep 1
done
echo "✅ MySQL pronto para conexões."


