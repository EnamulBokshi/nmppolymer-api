#!/bin/bash

#Build the project
echo "Building the project"

# Install dependencies
python3 -m pip install -r requirements.txt

# Make migrations and migrate
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files...."
python3 manage.py collectstatic --noinput --clear
