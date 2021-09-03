import os
from datetime import datetime
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string

TRANSACTION_TYPE_CHOICES = [
    (1, 'Débito'), (2, 'Boleto'), (3, 'Financiamento'), (4, 'Crédito'), (5, 'Recebimento Empréstimo'), (6, 'Vendas'),
    (7, 'Recebimento TED'), (8, 'Recebimento DOC'), (9, 'Aluguel'),
]

NATURE_TRANSACTION = {'addition': [1, 4, 5, 6, 7, 8], 'subtraction': [2, 3, 9]}

SUCCESS_UPLOAD = 'Dados injetados com sucesso.'

ERROR_INVALID_DATA = 'Arquivo em formato inválido.'


def cnab_validator(file):
    try:
        with open(file.name, 'r') as file:
            [mount_dict(line) for line in file.readlines()]
    except:  # noqa
        raise ValidationError(ERROR_INVALID_DATA)


def inject_data(file_name):
    with open(file_name, 'r') as file:
        data = [mount_dict(line) for line in file.readlines()]
        objects = [Operation(**data) for data in data]
        Operation.objects.bulk_create(objects)
    return data


def mount_dict(line):
    return {
        'transaction_type': line[0:1], 'date': datetime.strptime(line[1:9], '%Y%m%d'),
        'value': float(line[9:17] + '.' + line[17:19]), 'cpf': line[19:30], 'card': line[30:42],
        'hour': datetime.strptime(line[42:48], '%H%M%S'), 'owner': line[48:62], 'store': line[62:80]
    }


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

    def __str__(self):
        return self.store

    def get_nature_transaction(self):
        if self.transaction_type in NATURE_TRANSACTION['addition']:
            return 'Entrada'
        return 'Saída'

    class Meta:
        ordering = ['-created']
        verbose_name = 'Operação'
        verbose_name_plural = "Operações"


class CNABModel(BaseModel):
    file = models.FileField(verbose_name='Arquivo', upload_to=documents_directory_path, validators=[cnab_validator])

    def save(self, *args, **kwargs):
        inject_data(self.file.name)
        return super().save(args, kwargs)
