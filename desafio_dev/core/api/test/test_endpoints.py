from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy.mommy import make

from desafio_dev.core.models import Operation, SUCCESS_UPLOAD, ERROR_INVALID_DATA
from desafio_dev.core.api.serializers import CNABSerializer, OperationSerializer
from desafio_dev.core.api.views import OperationViewSet

factory = APIRequestFactory()


class OperationViewSetTestCase(TestCase):

    def setUp(self):
        self.user = make(get_user_model(), is_active=True)
        self.operations = make(Operation, _quantity=21)
        self.file = open(settings.BASE_DIR / 'CNAB.txt', 'r')
        self.file_invalid = open(settings.BASE_DIR / 'README.md', 'r')

    def test_create(self):
        data = {
            "transaction_type": 1, "date": "2019-03-01", "value": "192.00", "cpf": "84515254073",
            "card": "6777****1313", "hour": "17:27:12", "owner": "MARCOS PEREIRA", "store": "MERCADO DA AVENIDA"
        }
        request = factory.post('api/operation/', data)
        force_authenticate(request, user=self.user)
        view = OperationViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all(self):
        request = factory.get('api/operations/')
        force_authenticate(request, user=self.user)
        view = OperationViewSet.as_view({'get': 'list'})
        response = view(request)
        operations = Operation.objects.all()
        serializer = OperationSerializer(operations, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_operation(self):
        request = factory.get('api/operation/')
        force_authenticate(request, user=self.user)
        view = OperationViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.operations[0].id)
        operation = Operation.objects.get(pk=self.operations[0].id)
        serializer = OperationSerializer(operation)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            "transaction_type": 1, "date": "2019-03-01", "value": "192.00", "cpf": "84515254073",
            "card": "6777****1313", "hour": "17:27:12", "owner": "MARCOS PEREIRA", "store": "MERCADO DA AVENIDA"
        }
        request = factory.post('api/operation/', data)
        force_authenticate(request, user=self.user)
        view = OperationViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.operations[0].id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_upload_ok(self):
        data = {"file": self.file}
        request = factory.post('api/operation/upload', data)
        force_authenticate(request, user=self.user)
        view = OperationViewSet.as_view({'post': 'upload'})
        response = view(request)
        self.assertEquals(response.data['resultado'], SUCCESS_UPLOAD)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_upload_invalid(self):
        data = {"file": self.file_invalid}
        request = factory.post('api/operation/upload', data)
        force_authenticate(request, user=self.user)
        view = OperationViewSet.as_view({'post': 'upload'})
        response = view(request)
        self.assertEquals(response.data['resultado'], ERROR_INVALID_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
