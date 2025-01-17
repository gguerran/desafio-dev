#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 1
    done

    echo "PostgreSQL started"
fi

APP_HOME=`dirname $0`

cd $APP_HOME

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default.json
python manage.py runserver 0.0.0.0:8000
