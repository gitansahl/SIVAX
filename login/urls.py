from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='registrasi'),
    path('reg-warga/', views.register_warga, name='registrasi_warga'),
    path('reg-panitia/', views.register_panitia, name="registrasi panitia"),
    path('reg-admin/', views.register_admin, name='registrasi admin'),
]