from django.urls import path
from . import nakesviews


urlpatterns = [
    path( 'nakes/tiket_vaksin',nakesviews.read, name='tiket_vaksin'),
    path( 'nakes/detail_tiket_vaksin',nakesviews.detail_tiket, name='detail_tiket_vaksin'),
    path( 'pengguna/detail_kartu_vaksin',nakesviews.detail_kartu_vaksin, name='detail_kartu_vaksin'),
    path( 'nakes/ubah_status_tiket',nakesviews.update_tiket, name='ubah_status_tiket'),
    path( 'pengguna/kartu_vaksin',nakesviews.kartu_vaksin, name='kartu_vaksin'),
]
