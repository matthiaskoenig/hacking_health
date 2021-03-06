"""
Definition of REST API urls.
"""

from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from . import views

# schema_view = get_schema_view(title='API')  # Django rest framework
schema_view = get_swagger_view(title='API')  # Swagger

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'measurements', views.MeasurementViewSet, base_name='measurement')
router.register(r'recommendations', views.RecommendationViewSet, base_name='recommendation')

urlpatterns = [
    url(r'^$', schema_view, name="api"),
]
urlpatterns += router.urls
