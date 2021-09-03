from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse_lazy

from desafio_dev.core.models import ERROR_INVALID_DATA


class UploadOperationViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('core:upload')
        self.empty_form_data = {'file': ''}
        self.file = open(settings.BASE_DIR / 'CNAB.txt', 'r')
        self.file_invalid = open(settings.BASE_DIR / 'README.md', 'r')
        self.data = {'file': self.file}
        self.data_invalid = {'file': self.file_invalid}
        return super().setUp()

    def test_view_ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/upload.html')

    def test_form_error_empty_file(self):
        response = self.client.post(self.url, self.empty_form_data)
        self.assertFormError(response, 'form', 'file', ['Este campo é obrigatório.'])
        self.assertEquals(response.status_code, 200)

    def test_form_file_invalid(self):
        response = self.client.post(self.url, self.data_invalid)
        self.assertFormError(response, 'form', 'file', [ERROR_INVALID_DATA])
        self.assertEquals(response.status_code, 200)

    def test_form_ok(self):
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, 302)
