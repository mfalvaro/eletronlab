# coding: utf-8
"""
    Name:        forms.py
    Purpose:
    Author:      GPS-PC08
    Created:     01/05/2023
"""
##-----------------------------IMPORTS------------------------------------------
from django import forms

from django.forms import ModelForm

from estudoa.models import Tema, Coment, TemaComent

##-----------------------------GLOBALS------------------------------------------


##--------------------FUNCTIONS AND CLASSES-------------------------------------
# ##################################################################################################################################
##class EditTemaForm(ModelForm):
##    def clean_tema(self):
##       semana = self.cleaned_data['semana']
##
##       # Checa se o dado é válido.
##       if int(semana) < 1 or int(semana) > 52 :
##           raise ValidationError(_('Semana inválida - valor deve estar entre 1 e 52'))
##
##       # Remember to always return the cleaned data.
##       return semana
##
##    class Meta:
##        model = Tema
##        fields = '__all__'


# ##################################################################################################################################


# ##################################################################################################################################
