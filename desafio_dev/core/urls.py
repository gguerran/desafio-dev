from django.urls import path
from desafio_dev.core.views import UploadOperationView, ListOperationView

app_name = 'core'

urlpatterns = [
    path('', UploadOperationView.as_view(), name='upload'),
    path('list/', ListOperationView.as_view(), name='list'),
    path('list/<str:store>', ListOperationView.as_view(), name='list_by_store'),
]
