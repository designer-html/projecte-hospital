#!/bin/bash

BACKUP_FILE=$1
DB="hospital"

if [ -z "$BACKUP_FILE" ]; then
  echo "Uso: bash pg_restore_hospital.sh <backup_file>"
  exit 1
fi

sudo -u postgres dropdb $DB
sudo -u postgres createdb $DB
sudo -u postgres pg_restore -d $DB $BACKUP_FILE

echo "Restauración completada"

