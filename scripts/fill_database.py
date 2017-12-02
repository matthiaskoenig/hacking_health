"""
Initial setup of database.
"""
import os
import sys
import warnings
import numpy as np


FILE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PROJECT_DIR = os.path.join(FILE_DIR, "../gluconamics/")
DEFAULT_USER_PASSWORD = 'test'

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
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from collections import namedtuple
from diabot.models import Measurement, MeasurementTypeChoices, TissueChoices
from diabot.models import Recommendation
from analysis import data_mock

from diabot.models import rec_defs

################################################################################################################
UserDef = namedtuple('UserDef', ['username', 'first_name', 'last_name', 'email', 'status'])
user_defs = [
    UserDef("person_healthy", "Person", "Normal", "normal@diabot.de", "normal"),
    UserDef("person_impaired", "Person", "IGT", "igt@diabot.de", "igt"),
    UserDef("person_t2dm", "Person", "T2DM", "t2dm@diabot.de", "t2dm"),
    UserDef("test_user", "Test", "user", "test@diabot.de", "normal"),
]
################################################################################################################


def create_superuser():
    try:
        user = User.objects.get(username="mkoenig")
    except ObjectDoesNotExist:
        # User.objects.create_superuser('mkoenig', 'konigmatt@googlemail.com', os.environ['DJANGO_ADMIN_PASSWORD'])
        user = User.objects.create_superuser('mkoenig', 'konigmatt@googlemail.com', DEFAULT_USER_PASSWORD)
        user.last_name = "Matthias"
        user.first_name = "Koenig"
        user.save()


def create_recommendations(rec_defs):
    for rec_def in rec_defs:
        # create recommendation
        r = Recommendation(recommendation_id=uuid.uuid4(),
                           status=rec_def.status,
                           direction=rec_def.direction,
                           intervention=rec_def.intervention,
                           message=rec_def.message)
        r.save()
        print(r)


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
            # creates the user
            user = User.objects.create_user(username=user_def.username, email=user_def.email,
                                            password=DEFAULT_USER_PASSWORD)
            user.last_name = user_def.last_name
            user.first_name = user_def.first_name
            user.save()

            # creates example data
            add_measurements_for_user(user=user, status=user_def.status, N=10)


def add_measurements_for_user(user, status, N):
    """ Adds example measurement to database

    :return:
    """
    # create some mocked data for the subjects
    print("*** {} ***".format(user))
    samples = data_mock.create_samples(status=status, N=N)

    sensor_batch_id = uuid.uuid4()
    for sample in samples:
            measurement_id = uuid.uuid4()
            m = Measurement(user=user,
                            measurement_id=measurement_id,
                            sensor_batch_id=sensor_batch_id,
                            glucose=sample.glc,
                            insulin=sample.ins,
                            mtype=MeasurementTypeChoices.SINGLE,
                            tissue=TissueChoices.SALVIA)
            m.save()
            print("\t", m)


if __name__ == "__main__":
    create_superuser()
    create_users(user_defs=user_defs)
    create_recommendations(rec_defs=rec_defs)

