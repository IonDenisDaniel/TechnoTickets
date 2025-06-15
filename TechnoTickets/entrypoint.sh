#!/bin/bash 
#declaram ca e un bash script

APP_PORT=${PORT:-8000}

cd /app/

/app/migrate.sh

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm TechnoTickets.wsgi:application --bind "0.0.0.0:${APP_PORT}"