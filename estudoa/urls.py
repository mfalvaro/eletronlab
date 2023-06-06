# coding: utf-8
"""
    Name:        urls.py
    Purpose:
    Author:      GPS-PC08
    Created:     28/03/2023
"""
##-----------------------------IMPORTS------------------------------------------
from django.urls import path
from . import views


##----------------------------GLOBALS-------------------------------------------
urlpatterns = [
    path('', views.home, name='home'),
    path('temas/', views.TemaListViewSorted.as_view(), name='temas'), #Classe herdada com classificação nas colunas
    path('tema/<int:pk>', views.TemaDetailView.as_view(), name='tema-detail'),
    path('tema/<int:pk>/update/', views.TemaUpdate.as_view(), name='tema_update'),
    path('outrotema/', views.OutroTema, name='outro_tema'),

    path('coments/', views.ComentListView.as_view(), name='coments'),
    path('coment/<int:pk>', views.ComentDetailView.as_view(), name='coment-detail'),
    path('coments/create/', views.ComentCreate.as_view(), name='coment_create'),
    path('coment/<int:pk>/update/', views.ComentUpdate.as_view(), name='coment_update'),
    path('coment/<int:pk>/delete/', views.ComentDelete.as_view(), name='coment_delete'),

    path('searchs/', views.SearchListView.as_view(), name='searchs'),
    path('temacoment/<int:pk>', views.TemaComentDetailView.as_view(), name='temacoment-detail'),
    path('temacoments/create/', views.TemaComentCreate.as_view(), name='temacoment_create'),
    path('temacoment/<int:pk>/delete/', views.TemaComentDelete.as_view(), name='temacoment_delete'),

    path('cis/create/', views.CiCreate.as_view(), name='ci_create'),
    path('ci/<str:pk>/delete/', views.CiDelete.as_view(), name='ci_delete'),
    path('ci/<str:pk>/update/', views.CiUpdate.as_view(), name='ci_update'),

    ]

