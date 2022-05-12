#!/bin/bash
set -e

echo "PERFORMING BACKUP RESTORE"
psql -f $DB_BACKUP_FILE $DB_NAME