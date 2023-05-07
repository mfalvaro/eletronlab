# coding: utf-8
"""
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
"""
##-----------------------------IMPORTS------------------------------------------
from django.db import models
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse

##----------------------CLASSES AND FUNCTIONS ----------------------------------
# ########################################################################################################################################################################################
class Coment(models.Model):
    codcoment = models.AutoField(db_column='Codcoment', primary_key=True)  # Field name made lowercase.
    assunto = models.CharField(db_column='Assunto', max_length=255, blank=True, null=True, help_text='De maneira geral, do que trata o comentário?')  # Field name made lowercase.
    detalhe = models.CharField(db_column='Detalhe', max_length=255, blank=True, null=True, help_text='Descreva detalhes ...')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'coment'
        unique_together = (('assunto', 'detalhe'),)
        ordering = ['assunto', 'detalhe']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.assunto} :: {self.detalhe}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('coment-detail', args=[str(self.codcoment)])

# ########################################################################################################################################################################################
class Tema(models.Model):
    codtema = models.AutoField(db_column='Codtema', primary_key=True)  # Field name made lowercase.
    semana = models.SmallIntegerField(db_column='Semana', blank=True, null=True)  # Field name made lowercase.
    ordem = models.SmallIntegerField(db_column='Ordem', blank=True, null=True)  # Field name made lowercase.
    categoria = models.CharField(db_column='Categoria', max_length=15, blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pagina = models.IntegerField(db_column='Pagina', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tema'
        ordering = ['semana', 'ordem']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.semana}.{self.ordem} {self.titulo} ({self.categoria} {self.pagina})'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('tema-detail', args=[str(self.codtema)])

# ########################################################################################################################################################################################
class TemaComent(models.Model):
    codtema_coment = models.AutoField(db_column='Codtema_coment', primary_key=True)  # Field name made lowercase.
    tema = models.ForeignKey(Tema, models.DO_NOTHING, db_column='Tema', blank=True, null=True)  # Field name made lowercase.
    coment = models.ForeignKey(Coment, models.DO_NOTHING, db_column='Coment', blank=True, null=True)  # Field name made lowercase.
    data = models.DateTimeField(db_column='Data', blank=True, null=True, auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tema_coment'
        unique_together = (('tema', 'coment'),)
        ordering = ['tema', 'coment']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.tema.semana}.{self.tema.ordem} {self.tema.categoria} {self.tema.pagina}-{self.coment.assunto}::{self.coment.detalhe}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('temacoment-detail', args=[str(self.codtema_coment)])

# ########################################################################################################################################################################################
class Ci(models.Model):
    codci = models.CharField(db_column='Codci', primary_key=True, max_length=15, blank=True, null=False, help_text='Nome do circuito integrado')
    semana = models.IntegerField(db_column='Semana', blank=True, null=True)
    sobre = models.CharField(db_column='Sobre', max_length=75, blank=True, null=True, help_text='Sobre o circuito integrado')
    pinagem = models.CharField(db_column='Pinagem', max_length=25, blank=True, null=True, help_text='Figura da pinagem do ci')

    class Meta:
        managed = False
        db_table = 'ci'
        ordering = ['semana']

    def __str__(self):
        """String for representing the Model object."""
        return f'semana {self.semana} | ci {self.codci} - {self.sobre}'

