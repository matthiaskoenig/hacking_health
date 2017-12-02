from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Measurement

from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from .serializers import MeasurementSerializer, UserSerializer

##########################################
# Main views
##########################################
@login_required
def index_view(request):
    measurements = Measurement.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        'measurements': measurements,
    }
    return render(request, 'gluconamics/index.html', context)

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
    context = {
        'measurements': measurements,
    }
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
        This view should return a list of all measurement for the currently authenticated user.
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
    """ REST users.

    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    # filter_backends = (filters.DjangoFilterBackend, filters_rest.SearchFilter)
    # filter_fields = ('is_staff', 'username')
    # search_fields = ('is_staff', 'username', "email")
