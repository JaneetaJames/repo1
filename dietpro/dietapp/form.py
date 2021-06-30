from django import forms
from django.forms import ModelForm

from .models import dProfile, Fooditem


class Abc(forms.Form):
    profile_pic=forms.ImageField()


class fooditemForm(ModelForm):
    class Meta:
        model=Fooditem

        fields="__all__"

