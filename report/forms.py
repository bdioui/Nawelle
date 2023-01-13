from .models import import_dossiers, dossier, Note
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CSV_load(forms.ModelForm):
    class Meta:
        model = import_dossiers
        fields = ['import_op']

class dossier_form(forms.ModelForm):
    class Meta:
        model = dossier
        fields = '__all__'

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=("username", "password")

    def clean(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            password=self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Informations invalides.")

class Create_Note(forms.ModelForm):
    class Meta:
        model= Note
        fields= ['note']

