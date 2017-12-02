"""
Initial setup of database.
"""
import os
import sys
import warnings
import numpy as np


FILE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PROJECT_DIR = os.path.join(FILE_DIR, "../gluconamics/")
DEFAULT_USER_PASSWORD = 'diabot'

# setup django (add current path to sys.path)
path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../'))

if path not in sys.path:
    sys.path.append(path)

os.chdir(PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gluconamics.settings")
sys.path.append(PROJECT_DIR)

# django setup
import django
django.setup()

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from collections import namedtuple
from diabot.models import Measurement


################################################################################################################
UserDef = namedtuple('UserDef', ['username', 'first_name', 'last_name', 'email'])
user_defs = [
    UserDef("normal", "Person", "Normal", "normal@diabot.de"),
    UserDef("igt", "Person", "IGT", "igt@diabot.de"),
    UserDef("t2dm", "Person", "T2DM", "t2dm@diabot.de"),
]
################################################################################################################


def create_superuser():
    try:
        user = User.objects.get(username="mkoenig")
    except ObjectDoesNotExist:
        # User.objects.create_superuser('mkoenig', 'konigmatt@googlemail.com', os.environ['DJANGO_ADMIN_PASSWORD'])
        user = User.objects.create_superuser('mkoenig', 'konigmatt@googlemail.com', DEFAULT_USER_PASSWORD)
        print(user)


def create_users(user_defs):
    """ Create users in database from user definitions.

    :param delete_all: deletes all existing users
    :return:
    """
    # adds user to database
    for user_def in user_defs:
        try:
            user = User.objects.get(username=user_def.username)
        except ObjectDoesNotExist:
            user = User.objects.create_user(username=user_def.username, email=user_def.email,
                                            password=DEFAULT_USER_PASSWORD)
            user.last_name = user_def.last_name
            user.first_name = user_def.first_name
            user.save()
            print(user)


def add_measurements_to_database():
    """ Adds example measurement to database

    :return:
    """
    # normal measurements
    Nm = 10
    user = User.objects.get(username="normal")
    glc = np.random.rand(10)
    ins = np.random.rand(10)
    for k in range(Nm):
        m = Measurement(user=user,
                        measurement_id=k,
                        sensor_batch_id=1,
                        glucose=glc[k],
                        insulin=ins[k])
        m.save()


if __name__ == "__main__":
    create_superuser()
    create_users(user_defs=user_defs)
    add_measurements_to_database()
