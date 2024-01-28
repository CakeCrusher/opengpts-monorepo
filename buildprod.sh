#!/bin/bash

if [ -f .env ]; then
    echo "Loading .env file"
    cp .env frontend/.env
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

docker-compose -f docker-compose.prod.yml down

docker-compose -f docker-compose.prod.yml build --no-cache

echo "Finished building. Sleeping for 1 hour."
sleep 3600