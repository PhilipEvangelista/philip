from django.forms import ModelForm
from .models import Information, Account


class InfoRoom(ModelForm):
    class Meta:
        model = Information
        fields = ['age',
                  'birthday', ]


class UserRoom(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'