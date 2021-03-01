#!/bin/bash

echo "Starting up server"

python manage.py makemigrations core surveyor respondent authentication
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
