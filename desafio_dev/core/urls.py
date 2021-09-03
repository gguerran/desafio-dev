from django.urls import path
from desafio_dev.core.views import UploadOperationView

app_name = 'core'

urlpatterns = [
    path('', UploadOperationView.as_view(), name='upload')
]
