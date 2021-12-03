from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='registrasi'),
    path('reg-warga/', views.RegiterWargaView.as_view(), name='registrasi_warga'),
    path('reg-panitia/', views.RegiterPanitiaView.as_view(), name="registrasi panitia"),
    path('reg-admin/', views.RegiterAdminView.as_view(), name='registrasi admin'),
]