from django.urls import path
from . import panitia_views
from .admin_views import admin_distribusi_views, admin_penjadwalan_views, admin_vaksin_views

urlpatterns = [
    path('panitia/penjadwalan',panitia_views.index, name='panitia-penjadwalan'),
    path('panitia/penjadwalan/create',panitia_views.CreatePenjadwalan.as_view(), name='panitia-penjadwalan-create'),
    path('panitia/penjadwalan/detail/<str:kode_instansi>/<slug:tanggal>', panitia_views.DetailPenjadwalan.as_view(),  name='panitia-penjadwalan-detail'),
    path('panitia/penjadwalan/update/<str:kode_instansi>/<slug:tanggal>', panitia_views.UpdatePenjadwalan.as_view(),  name='panitia-penjadwalan-update'),
    
    path('admin/penjadwalan',admin_penjadwalan_views.index, name='admin-penjadwalan'),
    path('admin/penjadwalan/verifikasi/<str:kode_instansi>/<slug:tanggal>', admin_penjadwalan_views.VerifikasiPenjadwalan.as_view(),  name='admin-penjadwalan-verifikasi'),
    path('admin/penjadwalan/detail/<str:kode_instansi>/<slug:tanggal>', admin_penjadwalan_views.DetailPenjadwalan.as_view(),  name='admin-penjadwalan-detail'),
    path('admin/penjadwalan/update/<str:kode_instansi>/<slug:tanggal>', admin_penjadwalan_views.UpdatePenjadwalan.as_view(),  name='admin-penjadwalan-update'),
    
    path('admin/distribusi/create/<str:kode_instansi>/<slug:tanggal>',admin_distribusi_views.DistribusiPenjadwalan.as_view(),  name='admin-penjadwalan-distribusi'),
    path('admin/distribusi',admin_distribusi_views.Distribusi.as_view(), name='admin-distribusi'),
    path('admin/distribusi/detail/<str:kode_distribusi>',admin_distribusi_views.DetailDistribusi.as_view(),name='admin-distribusi-detail'),
    path('admin/distribusi/update/<str:kode_distribusi>',admin_distribusi_views.UpdateDistribusi.as_view(),name='admin-distribusi-update'),
    
    path('admin/vaksin',admin_vaksin_views.index, name='admin-vaksin'),
    path('admin/vaksin/update/<str:kode_vaksin>',admin_vaksin_views.UpdateStok.as_view(), name='admin-vaksin-update'),
]
