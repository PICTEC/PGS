#!/bin/bash
set -e

echo "PERFORMING BACKUP RESTORE"
psql -f /docker-entrypoint-initdb.d/pgs_postgres_backup postgres