#!/bin/bash
echo "Initializing Django server"
cd SRPA
echo "Pulling new changes from git repository"
git pull
echo "Installing requirements"
pip install -r requirements.txt
echo "Collecting static files"
python manage.py collectstatic -c --noinput
echo "Migrating databases"
python manage.py migrate
echo "Starting uwsgi"
uwsgi --ini web/SRPA_uwsgi.ini
