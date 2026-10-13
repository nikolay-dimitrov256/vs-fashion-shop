#!/bin/bash

set -euo pipefail

cd $HOME/webapps/vs-fashion-shop

git fetch origin

git checkout main

git reset --hard origin/main

cd fashionShop

docker compose pull app

docker compose up -d

docker exec nginx-container nginx -s reload