from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from desafio_dev.core.forms import CNABModelForm
from desafio_dev.core.models import CNABModel, SUCCESS_UPLOAD


class UploadOperationView(SuccessMessageMixin, CreateView):
    template_name = 'core/upload.html'
    form_class = CNABModelForm
    success_url = reverse_lazy('core:upload')
    success_message = SUCCESS_UPLOAD
    model = CNABModel
