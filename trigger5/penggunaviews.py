from django.http import response
from django.http.response import Http404
from django.shortcuts import render
from datetime import datetime, date
from django.views.generic.base import View
from django.utils.text import slugify
import json
import os
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

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

def read(request):
    response = {}
    data = getDummyData('tiket.json')['data']
    warga = getDummyData('warga.json')['data']
    contexts = []
    var_count = 0
    for datum in data:
        context = extractTiketVaksinPengguna(datum)
        contexts.append(context)
        times = datum['tgl_waktu']
        datetime_str = datetime.datetime.strptime(times, '%d/%m/%Y %H:%M')
        tbaru = datetime_str.strftime('%d %B %Y %H:%M')
        
        
        contexts[var_count]['tgl_waktu']= tbaru
        for w in warga:
            if w['email'] == datum['email']:
                contexts[var_count]['nama_penerima'] = w['nama_lengkap']
        var_count = var_count+1
    response['tiket'] = contexts
    return render(request, 'trigger5/nakes/Tiket/tiket_vaksin.html', response)