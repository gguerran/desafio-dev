from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from desafio_dev.core.models import Operation, ERROR_INVALID_DATA, SUCCESS_UPLOAD
from desafio_dev.core.api.serializers import OperationSerializer, CNABSerializer


class OperationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ['transaction_type', 'date', 'value', 'cpf', 'card', 'hour', 'owner', 'store']
    search_fields = ['transaction_type', 'date', 'value', 'cpf', 'card', 'hour', 'owner', 'store']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = Operation.objects.all()
    ordering = ('-created')
    parser_classes = (MultiPartParser, JSONParser)

    def get_serializer_class(self):
        if self.action == 'upload':
            return CNABSerializer
        return OperationSerializer

    @action(detail=False, methods=['post'])
    def upload(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        try:
            serializer.save()
            return Response({'resultado': SUCCESS_UPLOAD}, status=status.HTTP_201_CREATED)
        except:  # noqa
            return Response({'resultado': ERROR_INVALID_DATA}, status=status.HTTP_400_BAD_REQUEST)
