from django.db import connection
from django.http.response import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime, date
from django.urls.base import reverse
from django.views.generic.base import View
from django.utils.text import slugify
from trigger2.utils import getData

def extractOnePenjadwalanData(datum):
    context ={}
    context['nama_instansi'] = datum['nama_instansi']
    context['kode_instansi'] = datum['kode_instansi']
    context['waktu'] = datum['tanggal_waktu']
    context['slug_waktu'] = slugify(datum['tanggal_waktu'])
    context['kuota'] = datum['jumlah']
    context['kategori_penerima'] = datum['kategori_penerima']
    context['status'] = datum['status']
    context['lokasi_vaksin'] = datum['nama_lokasi']
    context['jumlah_nakes'] = datum['jumlah_nakes']
    context['email_admin'] = datum['email_admin']
    # bagian distribusi
    context['kode_distribusi']=datum['kode_distribusi']
    context['tanggal_distribusi'] = datum['tanggal']
    context['biaya'] = datum['biaya']
    context['jenis_vaksin']=datum['nama_vaksin']
    context['jumlah_vaksin'] = datum['jumlah_vaksin']
    return context

def deleteVaksin(request, kode_vaksin):
    print(kode_vaksin)
    with connection.cursor() as cursor:
        cursor.execute("delete from sivax.vaksin where kode=%s", [kode_vaksin])
    return HttpResponseRedirect(reverse('admin-vaksin'))

def index(request):
    if(request.session.get('role')):
        if("admin" not in request.session.get('role')):
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()
    response = {}
    data = getData(connection, 'vaksin')
    contexts = []
    for datum in data:
        contexts.append(datum)
    response['vaksin_records'] = contexts
    return render(request, 'trigger2/admin/vaksin/vaksin.html', response)

class UpdateStok(View):
    def get(self, request, *args, **kwargs):
        data = getData(connection, 'update_stok')
        kode_vaksin = kwargs['kode_vaksin']
        response = {}
        contexts = []
        for datum in data:
            if datum['kode_vaksin'].lower() == kode_vaksin.lower():
                contexts.append(datum)
        response['update_stok_records'] = contexts
        vaksin_records =  getData(connection, 'vaksin')
        for vaksin in vaksin_records:
            if vaksin['kode'].lower() == kode_vaksin.lower():
                response['nama_vaksin']= vaksin['nama']
        return render(request, 'trigger2/admin/vaksin/update-stok.html', response)
    
    def post(self, request, *args, **kwargs):
        idvaksn = kwargs['kode_vaksin']
        jumlah_vaksin = request.POST['jumlah']
        email = request.session['email']
        tanggal = datetime.now()
        print(tanggal)
        with connection.cursor() as cursor:
            cursor.execute("insert into sivax.update_stok values (%s, %s, %s, %s)",[email, tanggal, jumlah_vaksin, idvaksn])
            cursor.execute("update sivax.vaksin set stok = stok + %s where kode=%s", [jumlah_vaksin, idvaksn])
        return HttpResponseRedirect(reverse('admin-vaksin'))

