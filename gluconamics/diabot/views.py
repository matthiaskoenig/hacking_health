"""
Views.
"""
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Measurement, Recommendation

from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from .serializers import MeasurementSerializer, UserSerializer, RecommendationSerializer

##########################################
# Main views
##########################################
@login_required
def index_view(request):
    return user_view(request, user_id=request.user.pk)

@login_required
def recommendations_view(request):
    """ View the recommendations.

    :param request:
    :return:
    """
    recommendations = Recommendation.objects.all()
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'gluconamics/recommendations.html', context)

@login_required
def users_view(request):
    """ View the users.

    :param request:
    :return:
    """
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'gluconamics/users.html', context)

@login_required
def user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    measurements = Measurement.objects.filter(user=user).order_by('-timestamp')
    time = [m.timestamp.strftime('%Y-%m-%d %I:%M') for m in measurements]
    glc = [m.glucose for m in measurements]
    ins = [m.insulin for m in measurements]
    recommendations = [Recommendation.objects.all()[0]]
    context = {
        'measurements': measurements,
        'recommendations': recommendations,
        'user': user,
        'time': time,
        'glc': glc,
        'ins': ins,
    }
    if len(glc) > 0:
        context['glc_new'] = [glc[-1]]
        context['ins_new'] = [ins[-1]]
        context['time_new'] = [time[-1]]

    return render(request, 'gluconamics/index.html', context)


def about_view(request):
    return render(request, "gluconamics/about.html", {})


##########################################
# REST API
##########################################
# class MeasurementViewSet(viewsets.ModelViewSet):
class MeasurementViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    """ Set of measurements for the authenticated user. """
    permission_classes = (IsAuthenticated, )
    serializer_class = MeasurementSerializer
    lookup_field = 'measurement_id'

    def get_queryset(self):
        """
        This view returns a list of all measurement for the currently authenticated user.
        """
        user = self.request.user
        return Measurement.objects.filter(user=user).order_by('-timestamp')

    def perform_create(self, serializer):
        # automatically set the user on create
        serializer.save(user=self.request.user)



# class UserViewSet(viewsets.ModelViewSet):
class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """ Set of available users. """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    # filter_backends = (filters.DjangoFilterBackend, filters_rest.SearchFilter)
    # filter_fields = ('is_staff', 'username')
    # search_fields = ('is_staff', 'username', "email")


class RecommendationViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """ Set of recommendations. """
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Recommendation.objects.all()
    # filter_backends = (filters.DjangoFilterBackend, filters_rest.SearchFilter)
    # filter_fields = ('is_staff', 'username')
    # search_fields = ('is_staff', 'username', "email")
