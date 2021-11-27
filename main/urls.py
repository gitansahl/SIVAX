from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('distribusi-tugas/', views.distribusi_tugas, name='distribusi_tugas'),
    path('', views.landing_page, name='landing_page'),
]
