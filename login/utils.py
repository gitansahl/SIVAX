from collections import namedtuple
from django.db.utils import IntegrityError, DatabaseError, InternalError
def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def login(connection, email, password):
    if(email == "owner@gmail.com"):
        return ['admin', 'panitia', 'warga', 'nakes'] # super user agar testing mudah
    with connection.cursor() as cursor:
        cursor.execute("select * from sivax.pengguna where email=%s and password=%s", [email, password])
        result = namedtuplefetchall(cursor)
        if(result != []):
            result = []
            cursor.execute("select * from sivax.admin_satgas where email=%s", [email])
            if(cursor.fetchone()):
                result.append("admin")
            cursor.execute("select * from sivax.panitia_penyelenggara where email=%s", [email])
            if(cursor.fetchone()):
                result.append("panitia")
            cursor.execute("select * from sivax.warga where email=%s", [email])
            if( cursor.fetchone() ):
                result.append("warga")
            cursor.execute("select * from sivax.nakes where email=%s", [email])
            if(cursor.fetchone()):
                result.append("nakes")
    return result

def createPengguna(connection, POST):
    error = False
    with connection.cursor() as cursor:
        try:
            email = POST['email']
            noTelepon = POST['hp']
            password = POST['password']
            status = "sudah terverifikasi"
            cursor.execute("insert into sivax.pengguna values (%s,%s,%s,%s)", [email, noTelepon,password, status])
        except IntegrityError as e:
            error = "email "+POST['email']+" sudah terdaftarkan di sistem"
        except InternalError as e:
            i = str(e).find('CONTEXT')
            error = str(e)[0:i]
            print(error)
        except Exception as e:
            error = "Unexpected Error: "+str(e)
    return error

def createAdmin(connection, POST):
    error = False
    with connection.cursor() as cursor:
        try:
            email = POST['email']
            idPegawai = POST['noPetugas']
            cursor.execute("insert into sivax.admin_satgas values (%s,%s)", [email, idPegawai])
        except Exception as e:
            error = str(e)
            print(error)
            i = error.find('CONTEXT')
            # if(i != -1):
            #     error = str(e)[0:i]
    return error

def createPanitia(connection, POST):
    error = False
    with connection.cursor() as cursor:
        try:
            email = POST['email']
            namaLengkap = POST['namaLengkap']
            cursor.execute("insert into sivax.panitia_penyelenggara values (%s,%s)", [email, namaLengkap])
        except Exception as e:
            error = str(e)
            i = error.find('CONTEXT')
            # if(i != -1):
            #     error = str(e)[0:i]
    return error

def createNakes(connection, POST):
    error = False
    with connection.cursor() as cursor:
        try:
            email = POST['email']
            noSTR = POST['noSTR']
            tipe = POST['tipePetugas']
            cursor.execute("insert into sivax.nakes values (%s,%s,%s)", [email, noSTR, tipe])
        except Exception as e:
            error = str(e)
            i = error.find('CONTEXT')
            # if(i != -1):
            #     error = str(e)[0:i]
    return error

def deletePengguna(connection, email):
    with connection.cursor() as cursor:
        cursor.execute("delete from sivax.pengguna  where email=%s", [email])

def createWarga(connection,POST):
    error = False
    with connection.cursor() as cursor:
        try:
            email = POST['email']
            nik = POST['nik']
            nama_lengkap = POST['namaLengkap']
            jenis_kelamin=POST['jenisKelamin']
            noBangunan = POST['noBangunan']
            jalan=POST['namaJalan']
            kelurahan = POST['kelurahan']
            kecamatan=POST['kecamatan']
            kabkot=POST['kabkota']
            instansi=POST['instansi']
            cursor.execute("insert into sivax.warga values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [email,nik,nama_lengkap,jenis_kelamin,noBangunan,jalan,kelurahan,kecamatan,kabkot,instansi])
        except Exception as e:
            error = str(e)
            i = error.find('CONTEXT')
            # if(i != -1):
            #     error = str(e)[0:i]
    return error