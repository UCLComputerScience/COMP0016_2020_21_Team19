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

coverage run manage.py test
coverage report -m
coverage html
echo "The coverage report can be found in /htmlcov. Run `python3 -m htmlcov`"