from django.test import TestCase
from django.conf import settings
from django.core.files import File

from desafio_dev.core.models import Operation, CNABModel, mount_dict, inject_data


class OperationModelTestCase(TestCase):
    def setUp(self):
        self.data = inject_data(settings.BASE_DIR / 'CNAB.txt')
        self.operations = Operation.objects.all()
    
    def test_file_inject_count(self):
        self.assertEquals(len(self.data), self.operations.count())

    def test_transaction_type(self):
        field = Operation._meta.get_field('transaction_type')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_date(self):
        field = Operation._meta.get_field('date')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_value(self):
        field = Operation._meta.get_field('value')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEquals(field.max_digits, 10)
        self.assertEquals(field.decimal_places, 2)

    def test_cpf(self):
        field = Operation._meta.get_field('cpf')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEquals(field.max_length, 11)

    def test_card(self):
        field = Operation._meta.get_field('card')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEquals(field.max_length, 12)

    def test_owner(self):
        field = Operation._meta.get_field('owner')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEquals(field.max_length, 14)

    def test_store(self):
        field = Operation._meta.get_field('store')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertEquals(field.max_length, 19)
