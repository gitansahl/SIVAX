from django.http import response
from django.shortcuts import redirect, render
from django.db import connection
from django.contrib.messages.api import add_message
from django.contrib import messages
import datetime

# Create your views here.
def create_tiket(request, instansi, jadwal):
    with connection.cursor() as cursor:
        email = request.session.get('email')
        cursor.execute("SET search_path to sivax")
        cursor.execute(f"""
                       SELECT *
                       FROM WARGA
                       WHERE email = '{email}'
                       """)
        if len(cursor.fetchall()) == 0:
            messages.add_message(request, messages.WARNING, "Registrasi sebagai warga dahulu sebelum mendaftar vaksinasi")
            cursor.execute("SET search_path TO PUBLIC")
            return redirect("trigger4:detail_jadwal", instansi, jadwal)
        cursor.execute(f"""
                       SELECT kode
                       FROM INSTANSI
                       WHERE nama_instansi = '{instansi}'""")
        kode_instansi = cursor.fetchall()[0][0]
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM TIKET
                       """)
        data_no_tiket = cursor.fetchall()[0][0]
        no_tiket = 'tkt0' + str(data_no_tiket+1)
        try:
            cursor.execute(f"""
                           INSERT INTO TIKET(email, no_tiket, kode_instansi, kode_status, tgl_waktu) VALUES
                           ('{email}', '{no_tiket}', '{kode_instansi}', 01, '{jadwal}')""")
        except:
            messages.add_message(request, messages.WARNING, "Anda sudah vaksin dosis ke-2 atau vaksin dosis pertama Anda masih dalam rentang waktu 14 hari ke belakang")
            return redirect("trigger4:detail_jadwal", instansi, jadwal)
        cursor.execute("SET search_path to public")
    return redirect("trigger4:tiket_saya")

def detail_jadwal(request, instansi, jadwal):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO SIVAX")
        cursor.execute(f"""
                       SELECT kode
                       FROM INSTANSI
                       WHERE nama_instansi ='{instansi}'
                       """)
        kode_instansi = cursor.fetchall()[0][0]
        
        cursor.execute(f"""
                       SELECT *
                       FROM PENJADWALAN
                       WHERE kode_instansi = '{kode_instansi}' AND tanggal_waktu = '{jadwal}'""")
        penjadwalan = cursor.fetchall()[0]
        
        cursor.execute(f"""
                       SELECT nama
                       FROM LOKASI_VAKSIN
                       WHERE kode = '{penjadwalan[6]}'""")
        lokasi_vaksin = cursor.fetchall()[0][0]
        
        context = {
            'nama_instansi' : instansi,
            'jadwal' : jadwal,
            'kuota' : penjadwalan[2],
            'kategori' : penjadwalan[3],
            'nama_lokasi' : lokasi_vaksin,
        }
        cursor.execute("set search_path TO PUBLIC")
    return render(request, 'trigger4/pengguna/detail_jadwal.html', context)

def daftar_jadwal_terdaftar(request):
    context = dict()
    context['jadwal_vaksinasi'] = []
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO SIVAX")
        cursor.execute("""
                       SELECT *
                       FROM PENJADWALAN
                       WHERE status = 'pengajuan disetujui'
                       """)
        jadwal = cursor.fetchall()
        
        for i in range(len(jadwal)):
            cursor.execute("""
                           SELECT *
                           FROM INSTANSI
                           WHERE kode = %s""", [jadwal[i][0]])
            instansi = cursor.fetchall()
            context['jadwal_vaksinasi'].append([
                instansi[0][1], jadwal[i][1], jadwal[i][2]
            ])
        cursor.execute("SET search_path TO PUBLIC")
    return render(request, 'trigger4/pengguna/daftar_jadwal_terdaftar.html', context )

def tiket_saya(request):
    context = dict()
    context['kumpulan_tiket'] = []
    with connection.cursor() as cursor:
        email = request.session.get('email')
        cursor.execute("SET search_path to SIVAX")
        cursor.execute(f"""
                       SELECT * 
                       FROM TIKET
                       WHERE email = '{email}'
                       """)
        my_ticket = cursor.fetchall()
        
        for i in range(len(my_ticket)):
            cursor.execute("""
                           SELECT *
                           FROM INSTANSI
                           WHERE kode = %s""", [my_ticket[i][2]])
            instansi = cursor.fetchall()
            cursor.execute("""SELECT *
                           FROM STATUS_TIKET
                           WHERE kode = %s""", [my_ticket[i][3]])
            status_tiket = cursor.fetchall()
            context['kumpulan_tiket'].append([
                my_ticket[i][0], my_ticket[i][1], instansi[0][1], status_tiket[0][1], my_ticket[i][4]
            ])
        cursor.execute("SET search_path to public")
    return render(request, 'trigger4/pengguna/tiket_saya.html', context=context)

def detail_tiket(request, instansi, jadwal, nomor, status):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO SIVAX")
        cursor.execute(f"""
                       SELECT kode
                       FROM INSTANSI
                       WHERE nama_instansi = '{instansi}'
                       """)
        kode_instansi = cursor.fetchall()[0][0]
        cursor.execute(f"""
                       SELECT *
                       FROM PENJADWALAN
                       WHERE kode_instansi = '{kode_instansi}' AND tanggal_waktu = '{jadwal}'
                       """)
        penjadwalan = cursor.fetchall()[0]
        cursor.execute(f"""
                       SELECT nama
                       FROM LOKASI_VAKSIN
                       WHERE kode = '{penjadwalan[6]}'
                       """)
        nama_lokasi = cursor.fetchall()[0][0]
        
        context = {
            'nama_instansi' : instansi,
            'jadwal' : jadwal,
            'kuota' : penjadwalan[2],
            'kategori' : penjadwalan[3],
            'nama_lokasi' : nama_lokasi,
            'nomor_tiket' : nomor,
            'status_tiket' : status,
        }
        cursor.execute("SET search_path to public")
    return render(request, 'trigger4/pengguna/detail_tiket.html', context)

def tambah_vaksin(request):
    is_admin = False
    for i in request.session.get('roles'):
        if i == 'admin':
            is_admin = True
    if is_admin == False:
        return redirect("main:distribusi_tugas")
    
    context = dict()
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to SIVAX")
        cursor.execute("""SELECT COUNT(*)
                       FROM VAKSIN
                       """)
        data_kode = cursor.fetchall()[0][0]
        kode_vaksin = 'vcn0' + str(data_kode+1)
        context['kode_vaksin'] = kode_vaksin
        cursor.execute("SET search_path to public")
    
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("set search_path to sivax")
            try:
                cursor.execute(f"""
                               INSERT INTO VAKSIN (kode, nama, nama_produsen, no_edar, freq_suntik, stok) VALUES
                               ('{kode_vaksin}', '{request.POST["nama_vaksin"]}', '{request.POST["produsen"]}',
                               '{request.POST["no_edar"]}', '{request.POST["stok"]}', '{request.POST["frekuensi"]}')
                               """)
                return redirect("trigger2:admin-vaksin")
            except:
                messages.add_message(request, messages.WARNING, f"Sistem sedang tidak baik-baik saja, mohon coba lain waktu")
            cursor.execute("set search_path to public")
    return render(request, 'trigger4/admin/tambah_vaksin.html', context)

def delete_vaksin(request, kode):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO SIVAX")
        try:
            cursor.execute(f"""
                           DELETE FROM VAKSIN
                           WHERE kode = '{kode}'""")
        except:
            messages.add_message(request, messages.WARNING, f"Gagal menghapus Vaksin {kode}")
            cursor.execute("SET search_path TO PUBLIC")
        return redirect("trigger2:admin-vaksin")