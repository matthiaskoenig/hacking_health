#!/usr/bin/env bash
########################################################
# Setup the database
#
# Deletes old database and recreates all data.
########################################################
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# delete old database files & uploads
cd $DIR
cd ../gluconamics/
rm diabot.sqlite3
rm -rf diabot/migrations/*

# clean setup
python manage.py makemigrations
python manage.py makemigrations combine
python manage.py migrate


# clean everything
echo "* Remove upload files *"
rm media/*

echo "* Fill database with dummy data *"
cd $DIR
python fill_database.py

