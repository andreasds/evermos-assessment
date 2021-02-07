#!/bin/bash

echo "Setting up development environment"

root=$(pwd)

testing=online-store-test # testing container name
python_version=3.9.1-slim-buster # python version

# setup python environtment
echo ""
echo "### Installing python"
if [ ! $(docker ps -q -f name=$testing) ]; then
    if [ $(docker ps -q -f status=exited -f name=$testing) ]; then
        docker rm $testing
    fi
    docker run \
        -d \
        -it \
        -v $root:/home/testing \
        -w /home/testing \
        --rm \
        --name $testing \
        python:$python_version \
        bash
fi

# install python dependencies
echo ''
echo '### Installing python dependencies'
docker exec $testing bash -c "pip install requests"

# run application
echo ""
echo "Online Store Testing application"
docker exec \
    -it \
    $testing \
    python -m test.event1212

# destroy container
echo ""
echo "Destroy environment"
docker stop $testing

# DONE
echo ""
echo "DONE."
