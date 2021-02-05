#!/bin/bash

echo "Setting up environment"

root=$(pwd)

treasure_hunt=treasure-hunt # treasure hunt container name
python_version=3.9.1-slim-buster # python version

# setup python environtment
echo ""
echo "### Installing python"
if [ ! $(docker ps -q -f name=$treasure_hunt) ]; then
    if [ $(docker ps -q -f status=exited -f name=$treasure_hunt) ]; then
        docker rm $treasure_hunt
    fi
    docker run \
        -d \
        -it \
        -v $root:/home/treasure-hunt \
        -w /home/treasure-hunt \
        --rm \
        --name $treasure_hunt \
        python:$python_version \
        bash
fi

# run application
echo ""
echo "Treasure Hunt result"

# destroy container
echo ""
echo "Destroy environment"
docker stop $treasure_hunt

# DONE
echo ""
echo "DONE."
