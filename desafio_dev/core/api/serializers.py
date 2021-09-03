from django.core.exceptions import ValidationError

from rest_framework.serializers import ModelSerializer, Serializer, FileField

from desafio_dev.core.models import Operation, CNABModel, ERROR_INVALID_DATA


class OperationSerializer(ModelSerializer):

    class Meta:
        model = Operation
        exclude = []
        extra_kwargs = {'id': {'read_only': True}}


class CNABSerializer(Serializer):
    file = FileField()

    def create(self, validated_data):
        file = validated_data.get('file')
        try:
            cnab = CNABModel.objects.create(file=file)
            return cnab
        except:  # noqa
            raise ValidationError(ERROR_INVALID_DATA)
