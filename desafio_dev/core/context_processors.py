from desafio_dev.core.models import Operation


def stores(request):
    list_stores = Operation.objects.all().order_by('store').values_list('store', flat=True).distinct()
    return {'stores': list_stores}
