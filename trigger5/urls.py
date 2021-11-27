from django.urls import path
from . import nakesviews


urlpatterns = [
    path( 'nakes/tiket_vaksin',nakesviews.read, name='tiket_vaksin'),
    path( 'nakes/detail_tiket_vaksin',nakesviews.detail_tiket, name='detail_tiket_vaksin'),
    path( 'nakes/detail_jadwal',nakesviews.detail_jadwal, name='detail_tiket'),
    path( 'nakes/ubah_status_tiket',nakesviews.ubah_status_tiket, name='ubah_status_tiket'),
    path( 'pengguna/kartu_vaksin',nakesviews.kartu_vaksin, name='kartu_vaksin'),
]
