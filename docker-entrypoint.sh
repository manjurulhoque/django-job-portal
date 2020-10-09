#!/bin/bash

# Django Settings: A settings module can be specified by providing a value to the environment variable
# DJANGO_SETTINGS_MODULE for the container. If no value is specified,
# we use the development settings module by default
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-jobs.settings.development}
echo "Using DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE}"


# If the environment variable MIGRATE is a non-empty string, perform database migrations before starting
# the application.
if [ -n "$MIGRATE" ]; then
    echo "Performing DB migrations..."
    python manage.py migrate
fi

python manage.py runserver 0.0.0.0:8000
