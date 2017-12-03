#!/usr/bin/env bash
################################
# Deploy script
################################

git fetch --all
git reset --hard origin/develop
python manage.py collectstatic
sudo service gunicorn_hacking_health restart
