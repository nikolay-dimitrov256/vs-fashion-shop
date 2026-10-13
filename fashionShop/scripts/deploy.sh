#!/bin/sh

set -euo pipefail

cd /home/stryker/webapps/vs-fashion-shop

git fetch origin

git checkout main

git reset --hard origin/main

cd fashionShop

docker compose up -d --build

docker exec nginx-container nginx -s reload