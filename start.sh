#!/bin/bash

set -e

file_env() {
   local var="$1"
   local fileVar="${var}_FILE"
   local def="${2:-}"

   if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
      echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
      exit 1
   fi
   local val="$def"
   if [ "${!var:-}" ]; then
      val="${!var}"
   elif [ "${!fileVar:-}" ]; then
      val="$(< "${!fileVar}")"
   fi
   export "$var"="$val"
   unset "$fileVar"
}

file_env "DB_USER"
file_env "DB_PASSWORD"
file_env "EMAIL_HOST"
file_env "EMAIL_HOST_PASSWORD"
file_env "EMAIL_HOST_USER"
file_env "GOOGLE_CLIENT_ID"
file_env "GOOGLE_SECRET"
file_env "SECRET_KEY"

echo "Starting up server"

python manage.py makemigrations core surveyor respondent authentication
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --insecure