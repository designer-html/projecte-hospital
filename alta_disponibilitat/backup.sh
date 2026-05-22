#!/bin/bash

BACKUP_DIR="/var/backups/postgresql"
DB="hospital"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

pg_dump -Fc $DB > $BACKUP_DIR/${DB}_${DATE}.backup

# Eliminar backups antics (només mantenir els 5 últims)
cd $BACKUP_DIR
ls -1t *.backup | tail -n +6 | xargs rm -f
