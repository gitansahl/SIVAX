from django.urls import path

from . import views

app_name = 'trigger4'

urlpatterns = [
    path('pengguna/tiket/create', views.create_tiket, name='create_tiket'),
    path('pengguna/tiket/detail', views.detail_jadwal_daftar, name='detail_jadwal_daftar'),
    path('pengguna/tiket/tiket_saya', views.tiket_saya, name="tiket_saya"),
    path('pengguna/tiket/detail_tedaftar', views.detail_jadwal_terdaftar, name='detail_jadwal_terdaftar'),
    path('admin/vaksin/tambah_vaksin', views.tambah_vaksin, name="tambah_vaksin"),
]