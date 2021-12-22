from django.db import connection
from django.http import response
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
    context['kode_vaksin'] = datum['kode_vaksin']
    return context

def extractOneDistribusiData(datum):
    context={}
    context['kode'] = datum['kode']
    context['tanggal'] = datum['tanggal']
    context['biaya'] = datum['biaya']
    context['nama_vaksin'] = datum['nama_vaksin']
    context['kode_vaksin'] = datum['kode_vaksin']
    context['jumlah_vaksin'] = datum['jumlah_vaksin']
    return context

def deleteDistribusi(request, kode_distribusi):
    with connection.cursor() as cursor:
        cursor.execute("delete from sivax.distribusi where kode=%s",[kode_distribusi])
    return HttpResponseRedirect(reverse('admin-distribusi'))

class Distribusi(View):
    def get(self, request):
        if(request.session.get('roles')):
            if("admin" not in request.session.get('roles')):
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        data = getData(connection, 'distribusi')
        response={}
        contexts = []
        for datum in data:
            context = extractOneDistribusiData(datum)
            contexts.append(context)
        response['distribusi_records'] = contexts
        return render(request, 'trigger2/admin/distribusi/distribusi.html', response)

class UpdateDistribusi(View):
    def get(self, request, *args, **kwargs):
        if(request.session.get('roles')):
            if("admin" not in request.session.get('roles')):
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        response={}
        response['instansi_records'] = getData(connection, 'instansi')
        response['lokasi_records'] = getData(connection, 'lokasi')
        response['vaksin_records'] = getData(connection, 'vaksin')
        print(response['vaksin_records'])

        data = getData(connection, 'penjadwalan')
        kode_distribusi = kwargs['kode_distribusi']
        for datum in data:
            if datum['kode_distribusi'] == kode_distribusi:
                print(datum)
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context
        # print(context)

        return render(request, 'trigger2/admin/distribusi/update-distribusi.html', response)
    def post(self, request, *args, **kwargs):
        kode_distribusi = kwargs['kode_distribusi']
        x = request.POST
        with connection.cursor() as cursor:
            cursor.execute("set search_path to sivax")
            cursor.execute("update sivax.distribusi set tanggal=%s, biaya=%s, jumlah_vaksin=%s, kode_vaksin=%s where kode=%s"
            , [x['tanggal_waktu_distribusi'], x['biaya_distribusi'], x['jumlah_vaksin'], x['nama_vaksin'], kode_distribusi]
            )
        return HttpResponseRedirect(reverse('admin-distribusi'))

class DetailDistribusi(View):
    def get(self, request, *args, **kwargs):
        if(request.session.get('roles')):
            if("admin" not in request.session.get('roles')):
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        response={}
        response['instansi_records'] = getData(connection, 'instansi')
        response['lokasi_records']= getData(connection, 'lokasi')
        response['vaksin_records']=getData(connection, 'vaksin')

        data = getData(connection, 'penjadwalan')
        kode_distribusi = kwargs['kode_distribusi']
        for datum in data:
            if datum['kode_distribusi'] == kode_distribusi:
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/distribusi/detail-distribusi.html', response)

class DistribusiPenjadwalan(View):
    def get(self, request, *args, **kwargs):
        if(request.session.get('roles')):
            if("admin" not in request.session.get('roles')):
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        response={}
        response['instansi_records'] = getData(connection, 'instansi')
        response['lokasi_records'] = getData(connection, 'lokasi')
        response['vaksin_records'] = getData(connection, 'vaksin')

        data = getData(connection, 'penjadwalan')
        tanggal = kwargs['tanggal']
        for datum in data:
            if datum['kode_instansi'] == kwargs['kode_instansi'] and tanggal == slugify(datum['tanggal_waktu']):
                context = extractOnePenjadwalanData(datum)
        response['selected'] = context

        return render(request, 'trigger2/admin/distribusi/create-distribusi.html', response)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        x=request.POST

        with connection.cursor() as cursor:
            cursor.execute("set search_path to sivax")
            cursor.execute("update distribusi set tanggal=%s, biaya=%s, jumlah_vaksin=%s, kode_vaksin=%s where kode=%s"
            ,[x['tanggal_waktu_distribusi'], x['biaya_distribusi'], x['jumlah_vaksin'], x['nama_vaksin'], x['kode_distribusi']]
            )
            print("test")
        return HttpResponseRedirect(reverse('admin-distribusi'))
    
def verify(request):
    if(request.session.get('roles')):
        if("admin" not in request.session.get('roles')):
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()