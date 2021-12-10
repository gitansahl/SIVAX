from django.http import response
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime, date
from django.views.generic.base import View
from django.utils.text import slugify
import json
import os 
from django.urls import reverse, reverse_lazy
from django.db import connection
from .utils import getData
dir_path = os.path.dirname(os.path.realpath(__file__))

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
    data = getData(connection, "penjadwalan")
    contexts = []
    for datum in data:
        context = extractOnePenjadwalanData(datum)
        print(slugify(context['waktu']))
        contexts.append(context)
    response['penjadwalan_records'] = contexts
    return render(request, 'trigger2/panitia/penjadwalan.html', response)

class DetailPenjadwalan(View):
    def get(self, request, *args, **kwargs):
        data = getData(connection, "penjadwalan")
        tanggal = kwargs['tanggal']
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal == slugify(datum['tanggal_waktu']):
                context = extractOnePenjadwalanData(datum)
        response = {}
        response['data'] = context
        return render(request, 'trigger2/panitia/detail-penjadwalan.html', response)

class CreatePenjadwalan(View):
    def get(self, request, *args, **kwargs):
        response={}
        # response['instansi_records'] = getDummyData('instansi.json')['data']
        response['instansi_records'] = getData(connection, "instansi")
        # response['lokasi_records']= getDummyData('lokasi_vaksin.json')['data']
        response['lokasi_records'] = getData(connection, "lokasi")
        # print(response['instansi_records'])
        print("HEY")
        # print(response['lokasi_records'])
        return render(request, 'trigger2/panitia/create-penjadwalan.html', response)
    def post(self, request):
        print(request.POST)
        x = request.POST
        with connection.cursor() as cursor:
            cursor.execute("insert into sivax.penjadwalan values (%s, %s,%s, %s, %s, %s, %s)", [x['nama_instansi'], x['tanggal_waktu'], int(x['kuota']), x['penerima'], "pengiriman dikirim", 0, x['lokasi_vaksin'] ])
            print("success")
        return HttpResponseRedirect(reverse('panitia-penjadwalan'))

class UpdatePenjadwalan(View):
    def get(self, request, *args, **kwargs):
        response={}
        # response['instansi_records'] = getDummyData('instansi.json')['data']
        response['instansi_records'] = getData(connection, "instansi")
        # response['lokasi_records']= getDummyData('lokasi_vaksin.json')['data']
        response['lokasi_records'] = getData(connection, "lokasi")

        data = getData(connection, "penjadwalan")
        tanggal = kwargs['tanggal']
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal == slugify(datum['tanggal_waktu']):
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/panitia/update-penjadwalan.html', response)
    
    def post(self, request, *args, **kwargs):
        print(kwargs)
        response={'hasError':False}
        instansi = kwargs['kode_instansi']
        tanggal = kwargs['tanggal'][0:10]
        x=request.POST
        print(x)
        with connection.cursor() as cursor:
            cursor.execute("update sivax.penjadwalan set kode_instansi=%s, tanggal_waktu=%s, jumlah=%s, kategori_penerima=%s, kode_lokasi=%s where kode_instansi=%s and tanggal_waktu::date = %s"
            ,[x['nama_instansi'], x['tanggal_waktu'], x['kuota'], x['penerima'], x['lokasi_vaksin'], instansi, tanggal]
            )
        return HttpResponseRedirect(reverse('panitia-penjadwalan'))


def resendWithError(request, path, message):
    response = {'hasError': True, 'error': message}
    return render(request, path, message)
