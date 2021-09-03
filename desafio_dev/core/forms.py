from django.forms import ModelForm, FileInput

from desafio_dev.core.models import CNABModel


class CNABModelForm(ModelForm):

    class Meta:
        model = CNABModel
        fields = ['file']
        widgets = {'file': FileInput(attrs={'class': 'form-control'})}