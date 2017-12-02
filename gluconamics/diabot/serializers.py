"""
Model serialization used in the django-rest-framework.
"""

from rest_framework import serializers
from .models import Measurement
from django.contrib.auth.models import User

# TODO: querying a user should get the measurements


class MeasurementSerializer(serializers.ModelSerializer):
    """ Serializing all Measurements. """
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)

    class Meta:
        model = Measurement
        fields = ['user', 'timestamp', 'measurement_id', 'sensor_batch_id', 'glucose', 'insulin', 'tissue', 'mtype']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializing all Users. """
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']
