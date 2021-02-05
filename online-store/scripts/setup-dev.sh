#!/bin/bash

echo "Setting up development environment"

db=online-store-db # db container name
db_pwd=mysql-admin # db root password
db_version=8.0.22 # db version

# setup mysql database
echo ""
echo "### Installing MySQL database"
# docker stop $db
if [ ! $(docker ps -q -f name=$db) ]; then
    if [ $(docker ps -q -f status=exited -f name=$db) ]; then
        docker rm $db
    fi
    docker run \
        -d \
        -e MYSQL_ROOT_PASSWORD=$db_pwd \
        -p 17306:3306 \
        --restart unless-stopped \
        --name $db \
        mysql:$db_version
fi

db_ip=$(docker inspect $db | grep -w \"IPAddress\" | \
    head -n 1 | cut -d '"' -f 4)
# waiting mysql port ready
echo ""
printf "Initiating database"
while ! nc -z $db_ip 3306; do
    sleep 1
    printf "."
done
echo ""

# copy sql file
echo ""
echo "Creating online store database"
docker cp configs/db.sql $db:db.sql || \
    ( echo "ERROR: Please run script in project root folder" && exit )
docker exec $db bash -c "cat db.sql | \
    mysql -u root -p$db_pwd"
docker exec $db bash -c "rm db.sql"

# DONE
echo ""
echo "DONE."
