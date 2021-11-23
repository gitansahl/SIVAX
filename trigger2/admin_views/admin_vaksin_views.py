from django.http.response import Http404
from django.shortcuts import render
from datetime import datetime, date
from django.views.generic.base import View
from django.utils.text import slugify
import json
from trigger2.panitia_views import dir_path


def getDummyData(filename):
    try:
        with open(dir_path+"/DummyData/"+filename) as json_file:
            data = json.load(json_file)
            return data
    except:
        return {}

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

def index(request):
    response = {}
    data = getDummyData('vaksin.json')['data']
    contexts = []
    for datum in data:
        contexts.append(datum)
    response['vaksin_records'] = contexts
    return render(request, 'trigger2/admin/vaksin/vaksin.html', response)

class UpdateStok(View):
    def get(self, request, *args, **kwargs):
        data = getDummyData('update_stok.json')['data']
        kode_vaksin = kwargs['kode_vaksin']
        response = {}
        contexts = []
        for datum in data:
            if datum['kode_vaksin'].lower() == kode_vaksin.lower():
                contexts.append(datum)
        response['update_stok_records'] = contexts
        vaksin_records =  getDummyData('vaksin.json')['data']
        for vaksin in vaksin_records:
            if vaksin['kode'].lower() == kode_vaksin.lower():
                response['nama_vaksin']= vaksin['nama']
        return render(request, 'trigger2/admin/vaksin/update-stok.html', response)

