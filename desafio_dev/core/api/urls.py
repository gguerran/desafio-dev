from django.urls import path, include

from rest_framework import routers

from desafio_dev.core.api.views import OperationViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('operation', OperationViewSet, basename='operation')

urlpatterns = [
    path('', include(router.urls)),
]
