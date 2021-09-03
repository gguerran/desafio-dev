from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from desafio_dev.core.forms import CNABModelForm
from desafio_dev.core.models import Operation, CNABModel, SUCCESS_UPLOAD, NATURE_TRANSACTION


class UploadOperationView(SuccessMessageMixin, CreateView):
    template_name = 'core/upload.html'
    form_class = CNABModelForm
    success_url = reverse_lazy('core:upload')
    success_message = SUCCESS_UPLOAD
    model = CNABModel
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_page'] = True
        return context


class ListOperationView(ListView):
    template_name = 'core/list.html'
    model = Operation
    context_object_name = 'operations'

    def get_paginate_by(self, queryset):
        number_page = 10
        page = self.request.GET.get('number_page', '')
        if page:
            number_page = int(page)
        return number_page

    def get_queryset(self):
        store = self.kwargs.get('store', '')
        order_by = self.request.GET.get('order_by', '')
        queryset = Operation.objects.filter(store=store) if store else Operation.objects.all()
        return queryset.order_by(order_by) if order_by else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_page'] = True
        store = self.kwargs.get('store', '')
        if store:
            addictions = self.get_queryset().filter(
                transaction_type__in=NATURE_TRANSACTION['addition']).aggregate(Sum('value'))['value__sum'] or 0
            subtractions = self.get_queryset().filter(
                transaction_type__in=NATURE_TRANSACTION['subtraction']).aggregate(Sum('value'))['value__sum'] or 0
            total = addictions - subtractions
            context['total'] = '%.2f' % total
            context['store'] = store
        return context