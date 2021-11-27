from django.shortcuts import render

# Create your views here.
def create_tiket(request):
    return render(request, "trigger4/pengguna/create_tiket.html")
def detail_jadwal_daftar(request):
    return render(request, 'trigger4/pengguna/detail_jadwal_daftar.html')
def tiket_saya(request):
    return render(request, 'trigger4/pengguna/tiket_saya.html')
def detail_jadwal_terdaftar(request):
    return render(request, 'trigger4/pengguna/detail_jadwal_terdaftar')
def tambah_vaksin(request):
    return render(request, 'trigger4/admin/tambah_vaksin.html')
