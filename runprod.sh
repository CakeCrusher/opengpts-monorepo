#!/bin/bash

if [ -f .env ]; then
    echo "Loading .env file"
    cp .env frontend/.env
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

docker-compose -f docker-compose.prod.yml down

docker-compose -f docker-compose.prod.yml up