from django.urls import path

from . import views

app_name = 'trigger4'

urlpatterns = [
    path('pengguna/tiket/tiket_saya', views.tiket_saya, name='tiket_saya'),
    path('pengguna/tiket/detail/(?P<instansi>[0-9]+)$/(?P<jadwal>[0-9]+)$/(?P<nomor>[0-9]+)$/(?P<status>[0-9]+)$', views.detail_tiket, name='detail_tiket'),
    path('pengguna/penjadwalan/daftar_jadwal', views.daftar_jadwal_terdaftar, name="daftar_jadwal_terdaftar"),
    path('pengguna/penjadwalan/detail/(?P<instansi>[0-9]+)$/(?P<jadwal>[0-9]+)$', views.detail_jadwal, name='detail_jadwal'),
    path('pengguna/tiket/create/(?P<instansi>[0-9]+)$/(?P<jadwal>[0-9]+)$', views.create_tiket, name="create_tiket"),
    path('admin/vaksin/tambah_vaksin', views.tambah_vaksin, name="tambah_vaksin"),
]