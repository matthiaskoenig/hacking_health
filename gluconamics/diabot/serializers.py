"""
Model serialization used in the django-rest-framework.
"""

from rest_framework import serializers
from .models import Measurement, Recommendation
from django.contrib.auth.models import User


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


class RecommendationSerializer(serializers.ModelSerializer):
    """ Serializing all Recommendations. """

    class Meta:
        model = Recommendation
        fields = ['status', 'direction', 'intervention', 'message']
