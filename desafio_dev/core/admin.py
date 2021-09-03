from django.contrib import admin
from desafio_dev.core.models import Operation


class OperationAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'date', 'value', 'cpf', 'card', 'hour', 'owner', 'store']


admin.site.register(Operation, OperationAdmin)
