from django.db import connection
from django.http.response import Http404
from django.shortcuts import render
from datetime import datetime, date
from django.views.generic.base import View
from django.utils.text import slugify
import json
import os
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

def index(request):
    response = {}
    data = getData(connection, 'penjadwalan')
    contexts = []
    for datum in data:
        context = extractOnePenjadwalanData(datum)
        contexts.append(context)
    response['penjadwalan_records'] = contexts
    return render(request, 'trigger2/admin/penjadwalan/penjadwalan.html', response)

class DetailPenjadwalan(View):
    def get(self, request, *args, **kwargs):
        data = getData(connection, 'penjadwalan')
        tanggal = kwargs['tanggal']
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal == slugify(datum['tanggal_waktu']):
                context = extractOnePenjadwalanData(datum)
        response = {}
        response['data'] = context
        response['url']=kwargs
        return render(request, 'trigger2/admin/penjadwalan/detail-penjadwalan.html', response)

class UpdatePenjadwalan(View):
    def get(self, request, *args, **kwargs):
        response={}
        response['instansi_records'] = getData(connection, 'instansi')
        response['lokasi_records']= getData(connection, 'lokasi')

        data = getData(connection, 'penjadwalan')
        tanggal = kwargs['tanggal']
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal == slugify(datum['tanggal_waktu']):
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/penjadwalan/update-penjadwalan.html', response)

class VerifikasiPenjadwalan(View):
    def get(self, request, *args, **kwargs):
        response={}
        response['instansi_records'] = getData(connection, 'instansi')
        response['lokasi_records']= getData(connection, 'lokasi')

        data = getData(connection, 'penjadwalan')
        tanggal = kwargs['tanggal']
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal == slugify(datum['tanggal_waktu']):
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/penjadwalan/verifikasi-penjadwalan.html', response)

