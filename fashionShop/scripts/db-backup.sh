#!/bin/sh

docker exec -t vs-postgres-container pg_dump -U postgres -d vili_stil_db > "$HOME/backups/daily/db_backup_$(date +%y_%m_%d).sql"