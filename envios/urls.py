from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear/', views.crear_guia, name='crear_guia'),
    path('rastrear/', views.rastrear, name='rastrear_inicio'),
    path('rastrear/<str:numero>/', views.rastrear, name='rastrear'),
    path('buscar/', views.buscar_guia, name='buscar_guia'),
    path('guia/<str:numero>/vista/', views.guia_vista, name='guia_vista'),
    path('guia/<str:numero>/pdf/', views.guia_pdf, name='guia_pdf'),
]