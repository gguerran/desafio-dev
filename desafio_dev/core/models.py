import os
import uuid

from django.db import models
from django.utils.crypto import get_random_string

TRANSACTION_TYPE_CHOICES = [
    (1, 'Débito'), (2, 'Boleto'), (3, 'Financiamento'), (4, 'Crédito'), (5, 'Recebimento Empréstimo'), (6, 'Vendas'),
    (7, 'Recebimento TED'), (8, 'Recebimento DOC'), (9, 'Aluguel'),
]


def documents_directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    file_name = get_random_string(10, chars)
    return 'cnabs/{0}/{1}{2}'.format(instance.id, file_name, extension)


class BaseModel(models.Model):
    id = models.UUIDField(verbose_name='ID', primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField('criado em', auto_now_add=True)
    modified = models.DateTimeField('modificado em', auto_now=True)

    class Meta:
        abstract = True


class Operation(BaseModel):
    transaction_type = models.PositiveIntegerField(verbose_name='tipo de transação', choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField(verbose_name='data')
    value = models.DecimalField(verbose_name='valor', decimal_places=2, max_digits=10)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    card = models.CharField(verbose_name='cartão', max_length=12)
    hour = models.TimeField(verbose_name='hora')
    owner = models.CharField(verbose_name='dono da loja', max_length=14)
    store = models.CharField(verbose_name='nome da loja', max_length=19)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Operação'
        verbose_name_plural = "Operações"


class CNABModel(BaseModel):
    file = models.FileField(verbose_name='Arquivo', upload_to=documents_directory_path)