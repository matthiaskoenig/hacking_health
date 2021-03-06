#!/bin/bash

NAME="gluconamics"                              # Name of the application (*)
DJANGODIR=/var/git/hacking_health/gluconamics                  # Django project directory (*)
SOCKFILE=/var/git/hacking_health/run/gunicorn.sock # we will communicate using this unix socket (*)
USER=mkoenig                                         # the user to run as (*)
GROUP=mkoenig                                      # the group to run as (*)
NUM_WORKERS=1                                      # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=gluconamics.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=gluconamics.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /var/www/test/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/mkoenig/envs/hackhealth/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
