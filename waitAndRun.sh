#!/bin/sh
# waitAndRun.sh

set -e

until PGPASSWORD=$DB_MIGRATION_PASSWORD psql -h $DB_HOST -U $DB_USER_MIGRATION -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing commands"

>&2 echo "Creating database"
PGPASSWORD=$DB_MIGRATION_PASSWORD psql -h $DB_HOST -U $DB_USER_MIGRATION -c "CREATE DATABASE $DB_NAME;" || {
  >&2 echo "Cannot create database $DB_NAME"
}
PGPASSWORD=$DB_MIGRATION_PASSWORD psql -h $DB_HOST -U $DB_USER_MIGRATION -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER_RUNTIME;"

>&2 echo "Creating postgis extension"
PGPASSWORD=$DB_MIGRATION_PASSWORD psql -h $DB_HOST -U $DB_USER_MIGRATION $DB_NAME -c "CREATE EXTENSION postgis;" || {
  >&2 echo "Cannot create extension postgis"
}

>&2 echo "Make Migrations"
nohup python manage.py makemigrations
>&2 echo "Migrate"
nohup python manage.py migrate

>&2 echo "Create superuser"
nohup python manage.py create_init_user $DJANGO_SUPERUSER_USERNAME $DJANGO_SUPERUSER_EMAIL $DJANGO_SUPERUSER_PASSWORD


>&2 echo "Importing parking areas"
nohup python manage.py import_geojson_parking_areas $PARKING_AREAS_PATH $PARKING_AREAS_ADDRESS
>&2 echo "Importing payment zones"
nohup python manage.py import_geojson_payment_zones $PAYMENT_ZONES_PATH $PAYMENT_ZONES_ADDRESS
#>&2 echo "Import regions"
#nohup python manage.py import_geojson_regions $REGIONS_PATH $REGIONS_ADDRESS
#>&2 echo "Import parking terminals"
#nohup python manage.py import_parking_terminals $TERMINALS_ADDRESS $TERMINALS_LOCAL
#>&2 echo "Fill parking regions"
#nohup python manage.py fill_parking_regions

if [ "$CONSOLE_EMAIL" = TRUE ] ; then
  >&2 echo "Starting SMTP debugging server"
  export PYTHONUNBUFFERED=1
  nohup python -m smtpd -n -c DebuggingServer localhost:$EMAIL_PORT &
fi

>&2 echo "Starting server"
nohup python -u manage.py runserver 0.0.0.0:$SERVICE_PORT
