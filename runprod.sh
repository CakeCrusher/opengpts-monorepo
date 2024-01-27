#!/bin/bash

if [ -f .env ]; then
    echo "Loading .env file"
    cp .env frontend/.env
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

docker stop opengpts-monorepo_backendprod_1
docker stop opengpts-monorepo_frontendprod_1

docker-compose -f docker-compose.prod.yml up -d
