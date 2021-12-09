from django import forms
from django.db import connection

status = [('terdaftar', 'terdaftar'), ('siap vaksin', 'siap vaksin'),
('tidak lolos screening', 'tidak lolos screening'), ('selesai vaksin', 'selesai vaksin')]

class TiketVaksin(forms.Form):
    nama_instansi = forms.CharField(
        label=("Nama Instansi"), required=True, max_length=35)
    tanggal_dan_waktu = forms.DateTimeField(
        label=("Tanggal dan Waktu Pelaksanaan"), required=True)
    kuota = forms.IntegerField(
        label=("Kuota"))
    kategori_penerima = forms.CharField(
        label=("Kategori Penerima"), required=True, max_length=35)
    lokasi_vaksin = forms.CharField(
        label=("Lokasi Vaksin"), required=True, max_length=35)
    nomor_tiket = forms.CharField(max_length=15)
    status_tiket_update = forms.ChoiceField(
        choices = status, label=("Status Tiket"), required=True)
    status_tiket_detail = forms.CharField(
        label=("Status Tiket"), required=True)

    def __init__(self, *args, **kwargs):
        super(TiketVaksin, self).__init__(*args, **kwargs)
        self.fields['nama_instansi'].widget.attrs['readonly'] = True
        self.fields['nama_instansi'].widget.attrs['class'] = 'disabled'
        self.fields['tanggal_dan_waktu'].widget.attrs['readonly'] = True
        self.fields['tanggal_dan_waktu'].widget.attrs['class'] = 'disabled'
        self.fields['kuota'].widget.attrs['readonly'] = True
        self.fields['kuota'].widget.attrs['class'] = 'disabled'
        self.fields['kategori_penerima'].widget.attrs['readonly'] = True
        self.fields['kategori_penerima'].widget.attrs['class'] = 'disabled'
        self.fields['lokasi_vaksin'].widget.attrs['readonly'] = True
        self.fields['lokasi_vaksin'].widget.attrs['class'] = 'disabled'
        self.fields['nomor_tiket'].widget.attrs['readonly'] = True
        self.fields['nomor_tiket'].widget.attrs['class'] = 'disabled'
        self.fields['status_tiket_detail'].widget.attrs['readonly'] = True
        self.fields['status_tiket_detail'].widget.attrs['class'] = 'disabled'
        


        
