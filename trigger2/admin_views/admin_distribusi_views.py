from django.http import response
from django.http.response import Http404
from django.shortcuts import render
from datetime import datetime, date
from django.views.generic.base import View
from django.utils.text import slugify
import json
import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
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

def extractOneDistribusiData(datum):
    context={}
    context['kode'] = datum['kode']
    context['tanggal'] = datum['tanggal']
    context['biaya'] = datum['biaya']
    context['nama_vaksin'] = datum['nama_vaksin']
    context['jumlah_vaksin'] = datum['jumlah_vaksin']
    return context

class Distribusi(View):
    def get(self, request):
        data = getDummyData('distribusi.json')['data']
        response={}
        contexts = []
        for datum in data:
            context = extractOneDistribusiData(datum)
            contexts.append(context)
        response['distribusi_records'] = contexts
        return render(request, 'trigger2/admin/distribusi/distribusi.html', response)

class UpdateDistribusi(View):
    def get(self, request, *args, **kwargs):
        response={}
        response['instansi_records'] = getDummyData('instansi.json')['data']
        response['lokasi_records']= getDummyData('lokasi_vaksin.json')['data']
        response['vaksin_records']=getDummyData('vaksin.json')['data']

        data = getDummyData('penjadwalan_v2.json')['data']
        kode_distribusi = kwargs['kode_distribusi']
        for datum in data:
            if datum['kode_distribusi'] == kode_distribusi:
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/distribusi/update-distribusi.html', response)

class DetailDistribusi(View):
    def get(self, request, *args, **kwargs):
        response={}
        response['instansi_records'] = getDummyData('instansi.json')['data']
        response['lokasi_records']= getDummyData('lokasi_vaksin.json')['data']
        response['vaksin_records']=getDummyData('vaksin.json')['data']

        data = getDummyData('penjadwalan_v2.json')['data']
        kode_distribusi = kwargs['kode_distribusi']
        for datum in data:
            if datum['kode_distribusi'] == kode_distribusi:
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/distribusi/detail-distribusi.html', response)

class DistribusiPenjadwalan(View):
    def get(self, request, *args, **kwargs):
        response={}
        response['instansi_records'] = getDummyData('instansi.json')['data']
        response['lokasi_records']= getDummyData('lokasi_vaksin.json')['data']
        response['vaksin_records']=getDummyData('vaksin.json')['data']

        data = getDummyData('penjadwalan_v2.json')['data']
        tanggal = kwargs['tanggal'][0:10]
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal in datum['tanggal_waktu']:
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/distribusi/create-distribusi.html', response)