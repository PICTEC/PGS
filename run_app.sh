#!/bin/sh
# run_app.sh

set -e

until PGPASSWORD=$DB_MIGRATION_PASSWORD psql -h $DB_HOST -U $DB_USER_MIGRATION -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - starting app"

>&2 echo "Migrate"
nohup python manage.py migrate

if [ "$CONSOLE_EMAIL" = TRUE ] ; then
  >&2 echo "Starting SMTP debugging server"
  export PYTHONUNBUFFERED=1
  nohup python -m smtpd -n -c DebuggingServer localhost:$EMAIL_PORT &
fi

>&2 echo "Copy static files"
python manage.py collectstatic --noinput

>&2 echo "Starting server"
nohup python -u manage.py runserver 0.0.0.0:$SERVICE_PORT
