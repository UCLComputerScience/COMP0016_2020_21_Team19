#!/bin/bash
python manage.py migrate
python manage.py runserver 0:80
echo Running Django on the localhost at http://localhost:9000