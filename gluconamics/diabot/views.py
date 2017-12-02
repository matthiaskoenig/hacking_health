from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Measurement

from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .serializers import MeasurementSerializer

##########################################
# Main views
##########################################
@login_required
def index_view(request):
    measurements = Measurement.objects.filter(user=request.user)
    context = {
        'measurements': measurements,
    }
    return render(request, 'gluconamics/index.html', context)


def about_view(request):
    return render(request, "gluconamics/about.html", {})


##########################################
# REST API
##########################################
class MeasurementViewSet(viewsets.ModelViewSet):
    """ REST archives.

    lookup_field defines the url of the detailed view.
    permission_classes define which users is allowed to do what.
    """
    # TODO: filter based on user
    queryset = Measurement.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = MeasurementSerializer
    lookup_field = 'measurement_id'
    # filter_backends = (filters.DjangoFilterBackend, filters_rest.SearchFilter)
    # filter_fields = ('name', 'task_id', 'tags', 'created')
    # search_fields = ('name', 'tags__name', 'created')

    def perform_create(self, serializer):
        # automatically set the user on create
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """ REST users.

    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    # filter_backends = (filters.DjangoFilterBackend, filters_rest.SearchFilter)
    # filter_fields = ('is_staff', 'username')
    # search_fields = ('is_staff', 'username', "email")
