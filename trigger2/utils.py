
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getData(connection, command):
    "Return sql query based on command"
    context = {'hasError': False}
    with connection.cursor() as cursor:
        try:
            cursor.execute("set search_path to sivax")
            cursor.execute(commandMap[command])
            context = dictfetchall(cursor)
        except Exception as e:
            print(e)
            context['hasError'] = True
            context['error'] = str(e)
    return context

commandMap = {
    'penjadwalan': "select * from (select kode as kode_lokasi, nama as nama_lokasi from lokasi_vaksin) as temp5 natural join (select * from (select kode as kode_instansi, nama_instansi from instansi) as temp3 natural join (select * from penjadwalan p left outer join (select d.kode as kode_distribusi, d.tanggal, d.biaya, d.jumlah_vaksin, d.kode_vaksin, v.nama as nama_vaksin, v.stok from distribusi d join vaksin v on d.kode_vaksin=v.kode) as temp1 on p.kode_distribusi=temp1.kode_distribusi) as temp2) as temp4",
    "distribusi":"select d.kode, tanggal, biaya, jumlah_vaksin, kode_vaksin, nama as nama_vaksin from distribusi d, vaksin v where d.kode_vaksin=v.kode",
    "instansi":"select kode, nama_instansi from instansi",
    "lokasi_vaksin":"select * from lokasi_vaksin",
    "lokasi":"select * from lokasi_vaksin",
    "update_stok":"select * from update_stok",
    "vaksin":"select * from vaksin"
}