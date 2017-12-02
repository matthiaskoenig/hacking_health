"""
Definition of REST API urls.
"""

from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from . import views

from gluconamics import

# schema_view = get_schema_view(title='Tellurium Web API')  # Django rest framework
schema_view = get_swagger_view(title='API')  # Swagger

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'measurments', views.MeasurementViewSet, base_name='tag')

urlpatterns = [
    url(r'^$', schema_view),
]
urlpatterns += router.urls
