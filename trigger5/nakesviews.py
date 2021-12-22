from django.http import response
from django.http.response import Http404
from django.shortcuts import render, redirect
from datetime import datetime, date
from django.views.generic.base import View
from django.utils.text import slugify
import json
import os
import datetime
from django.db import connection
from collections import namedtuple
from .forms import *


dir_path = os.path.dirname(os.path.realpath(__file__))

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def getDummyData(filename):
    try:
        with open(dir_path+"/DummyData/"+filename) as json_file:
            data = json.load(json_file)
            return data
    except:
        return {}

def extractTiketVaksinPengguna(datum):
    context={}
    context['email'] = datum['email']
    context['no_tiket'] = datum['no_tiket']
    context['kode_instansi'] = datum['kode_instansi']
    context['kode_status'] = datum['kode_status']
    context['tgl_waktu'] = datum['tgl_waktu']
    return context

def extractKartuVaksin(datum):
    context={}
    context['email'] = datum['email']
    context['no_sertifikat'] = datum['no_sertifikat']
    context['no_tiket'] = datum['no_tiket']
    context['status_tahapan'] = datum['status_tahapan']
    return context


def read(request):
    response = {}
    # data = getDummyData('tiket.json')['data']
    # warga = getDummyData('warga.json')['data']
    # status_tiket =  getDummyData('status_tiket.json')['data']
    # contexts = []
    # var_count = 0
    # for datum in data:
    #     context = extractTiketVaksinPengguna(datum)
    #     contexts.append(context)
    #     times = datum['tgl_waktu']
    #     datetime_str = datetime.datetime.strptime(times, '%d/%m/%Y %H:%M')
    #     tbaru = datetime_str.strftime('%d %B %Y %H:%M')
    #     contexts[var_count]['tgl_waktu']= tbaru

    #     for w in warga:
    #         if w['email'] == datum['email']:
    #             contexts[var_count]['nama_penerima'] = w['nama_lengkap']
    #     for st in status_tiket:
    #         if st['kode'] == datum['kode_status']:
    #             contexts[var_count]['status_tiket'] = st['nama_status']
    #     var_count = var_count+1
    # response['tiket'] = contexts

    simpan_roles = request.session.get('roles')
    with connection.cursor() as cursor:
        if 'warga' in simpan_roles:
            email_pengguna = request.session.get('email')
            cursor.execute(
                f"SELECT instansi from SIVAX.WARGA WHERE email = '{email_pengguna}'")
            kode_instansi = cursor.fetchone()
            cursor.execute(
                f"SELECT no_tiket, nama_lengkap, tgl_waktu, nama_status FROM SIVAX.TIKET T, SIVAX.WARGA W, SIVAX.STATUS_TIKET ST, SIVAX.PENJADWALAN P WHERE T.email = W.email AND T.kode_status = ST.kode AND T.tgl_waktu = P.tanggal_waktu AND P.kode_instansi = '{kode_instansi[0]}'")
            hasil_tiket = namedtuplefetchall(cursor)
            response['tiket_vaksin'] = hasil_tiket
    return render(request, 'trigger5/nakes/Tiket/tiket_vaksin.html', response)

def detail_tiket(request):
    response = {}
    nomor_tiket = request.GET.get('nt')
    # print("-------------------------------------"+nomor_tiket)
    with connection.cursor() as cursor:
        cursor.execute(
            f"select nama_instansi, tgl_waktu, jumlah, kategori_penerima, nama, nama_status from SIVAX.TIKET AS T LEFT OUTER JOIN SIVAX.PENJADWALAN AS P ON T.tgl_waktu = P.tanggal_waktu LEFT OUTER JOIN SIVAX.LOKASI_VAKSIN AS LV ON P.kode_lokasi = LV.kode LEFT OUTER JOIN SIVAX.INSTANSI AS I ON P.kode_instansi = I.kode LEFT OUTER JOIN SIVAX.STATUS_TIKET AS ST ON T.kode_status = ST.kode WHERE T.no_tiket = '{nomor_tiket}'")
        #buat ngambil datanya pake fetchone()
        hasil_detail = cursor.fetchone() 
        # print(hasil_detail)
        data_form = {}
        data_form['nama_instansi'] = hasil_detail[0]
        data_form['tanggal_dan_waktu'] = hasil_detail[1]
        data_form['kuota'] = hasil_detail[2]
        data_form['kategori_penerima'] = hasil_detail[3]
        data_form['lokasi_vaksin'] = hasil_detail[4]
        data_form['nomor_tiket'] = nomor_tiket
        data_form['status_tiket_detail'] = hasil_detail[5]
        #masukin dict tdi menjadi nilai di form(isi form)
        form = TiketVaksin(initial = data_form)
        #from masukin ke response
        response['form'] = form
    return render(request, 'trigger5/nakes/Tiket/detail_tiket_vaksin.html', response)

def update_tiket(request):
    response = {}
    #pake method get
    if request.method == 'GET':
        notkt = request.GET.get('tn')
        print("-------------------------------------"+notkt)
        with connection.cursor() as cursor:
            cursor.execute(
                f"select nama_instansi, tgl_waktu, jumlah, kategori_penerima, nama, nama_status from SIVAX.TIKET AS T LEFT OUTER JOIN SIVAX.PENJADWALAN AS P ON T.tgl_waktu = P.tanggal_waktu LEFT OUTER JOIN SIVAX.LOKASI_VAKSIN AS LV ON P.kode_lokasi = LV.kode LEFT OUTER JOIN SIVAX.INSTANSI AS I ON P.kode_instansi = I.kode LEFT OUTER JOIN SIVAX.STATUS_TIKET AS ST ON T.kode_status = ST.kode WHERE T.no_tiket = '{notkt}'")
            #buat ngambil datanya pake fetchone()
            hasil_detail = cursor.fetchone() 
            # print("--------------------hasil detail :"+hasil_detail[0])
            data_form = {}
            data_form['nama_instansi'] = hasil_detail[0]
            data_form['tanggal_dan_waktu'] = hasil_detail[1]
            data_form['kuota'] = hasil_detail[2]
            data_form['kategori_penerima'] = hasil_detail[3]
            data_form['lokasi_vaksin'] = hasil_detail[4]
            data_form['nomor_tiket'] = notkt
            data_form['status_tiket_detail'] = hasil_detail[5]
            data_form['status_tiket_update'] = hasil_detail[5]
            #masukin dict tdi menjadi nilai di form(isi form)
            form = TiketVaksin(initial = data_form)
            #from masukin ke response
            response['form'] = form
    else:
        #jika klik update, maka pake post 
        nomor_tkt = request.POST['nomor_tiket']
        with connection.cursor() as cursor:
            #ambil data form
            ubah_status = request.POST['status_tiket_update']
            cursor.execute(
                f"select kode from SIVAX.STATUS_TIKET WHERE nama_status = '{ubah_status}'")
            kode_stat = cursor.fetchone()
            print("-----------------------------kode status: "+kode_stat[0])
            cursor.execute(
                f"update SIVAX.TIKET set kode_status = '{kode_stat[0]}' WHERE no_tiket = '{nomor_tkt}'")
        # kalo udha selesai update redirect ke halaman tiket vaksin
        return redirect('tiket_vaksin')     
    return render(request, 'trigger5/nakes/Tiket/ubah_status_tiket.html', response)




# def detail_tiket(request):
#     response = {}
#     data = getDummyData('tiket.json')['data']
#     instansi = getDummyData('instansi.json')['data']
#     status_tiket =  getDummyData('status_tiket.json')['data']
#     contexts = []
#     var_count = 0
#     for datum in data:
#         context = extractTiketVaksinPengguna(datum)
#         contexts.append(context)
#         times = datum['tgl_waktu']
#         datetime_str = datetime.datetime.strptime(times, '%d/%m/%Y %H:%M')
#         tbaru = datetime_str.strftime('%d %B %Y %H:%M')
        
        
#         contexts[var_count]['tgl_waktu']= tbaru
#         for i in instansi:
#             if i['kode'] == datum['kode_instansi']:
#                 contexts[var_count]['nama_instansi'] = i['nama_instansi']
#         for st in status_tiket:
#             if st['kode'] == datum['kode_status']:
#                 contexts[var_count]['status_tiket'] = st['nama_status']
#         var_count = var_count+1
#     response['detail_tiket'] = contexts
#     return render(request, 'trigger5/nakes/Tiket/detail_tiket_vaksin.html', response)

def kartu_vaksin(request):
    response = {}
    with connection.cursor() as cursor:
        email_pengguna = request.session.get('email')
        cursor.execute(
            f"SELECT no_sertifikat,status_tahapan from SIVAX.KARTU_VAKSIN WHERE email = '{email_pengguna}'")
        #ambil banyak
        hasil_kartu_vaksin = namedtuplefetchall(cursor)
        # print(hasil_kartu_vaksin)
        response['kartu_vaksin'] = hasil_kartu_vaksin
    return render(request, 'trigger5/pengguna/tiket saya/kartu_vaksin.html', response)

def detail_kartu_vaksin(request):
    response = {}
    stat_tahapan = request.GET.get('st')
    no_sertif = request.GET.get('ns')
    # print("-------------------------------------"+nomor_tiket)
    with connection.cursor() as cursor:
        #data sesuai emailnya, 
        email_pengguna = request.session.get('email')
        cursor.execute(
            f"SELECT nama_lengkap FROM SIVAX.WARGA WHERE email= '{email_pengguna}'")
        #buat ngambil datanya pake fetchone() amnil satu aja
        nama = cursor.fetchone() 
        response['kv_nama'] = nama[0]
        response['kv_no_sertif'] = no_sertif
        response['kv_stat_tahapan'] = stat_tahapan
    return render(request, 'trigger5/pengguna/tiket saya/detail_kartu_vaksin.html', response)





