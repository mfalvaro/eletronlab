# coding: utf-8
"""
    Name:        forms.py
    Purpose:
    Author:      GPS-PC08
    Created:     01/05/2023
"""
##-----------------------------IMPORTS------------------------------------------
from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from estudoa.models import Tema, Coment, TemaComent

##-----------------------------GLOBALS------------------------------------------


##--------------------FUNCTIONS AND CLASSES-------------------------------------
# ##################################################################################################################################
class ComentCreateForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ['assunto', 'detalhe']

    def clean_assunto(self):
        data = self.cleaned_data["assunto"]
        data = data.lower().strip()
        return data # sempre retorne o valor, mesmo que não tenha sido modificado

    def clean_detalhe(self):
        data = self.cleaned_data['detalhe']
        data = data.lower().strip()
        if 'transistor' in data:
            #raise ValidationError("Corrrija a acentuação!")
            data = data.replace('transistor','transístor')
        return data # sempre retorne o valor, mesmo que não tenha sido modificado

