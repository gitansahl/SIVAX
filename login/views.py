from django.shortcuts import render
from django.views.generic.base import View
from django.db import connection
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from .utils import createAdmin, createNakes, createPanitia, createPengguna, createWarga, login, deletePengguna

class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
        
    def post(self,request):
        error = {}
        result = login(connection, request.POST.get('email'), request.POST.get('password'))
        if(result == []):
            error['not_exists'] = True
            return render(request, 'login.html', error)
        print(result)
        request.session['email'] = request.POST.get('email')
        request.session['roles'] = result
        return HttpResponseRedirect(reverse('main:distribusi_tugas'))

def register(request):
    if(request.method=='POST'):
        return HttpResponseRedirect('/trigger1/'+request.POST['akun'])
    return render(request, 'register.html')

class RegiterWargaView(View):
    def get(self, request):
        context = {}
        context['instansis'] = dict(getAllInstansi())
        return render(request, 'register_warga.html', context)

    def post(self, request):
        context = {}
        error = createPengguna(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        error = createWarga(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        return HttpResponseRedirect(reverse('login:login')) 

class RegiterPanitiaView(View):
    def get(self, request):
        context = {}
        context['instansis'] = dict(getAllInstansi())
        return render(request, 'register_panitia.html', context)

    def post(self, request):
        context = {}
        error = createPengguna(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        error = createPanitia(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        error = createWarga(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        if(request.POST['isNakes'] == 'TIDAK'):
            return HttpResponseRedirect(reverse('login:login')) 
        error = createNakes(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        return HttpResponseRedirect(reverse('login:login')) 

class RegiterAdminView(View):
    def get(self, request):
        context = {}
        context['instansis'] = dict(getAllInstansi())
        return render(request, 'register_admin.html',context)

    def post(self, request):
        context = {}
        error = createPengguna(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        error = createAdmin(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        error = createWarga(connection, request.POST)
        if(error):
            return resendWithError(request, context, error)
        return HttpResponseRedirect(reverse('login:login')) 

def resendWithError(request, context, message):
    context['error'] = True
    context['message'] = message
    context['instansis'] = dict(getAllInstansi())
    deletePengguna(connection, request.POST['email'])
    return render(request, 'register_admin.html',context)       

def getAllInstansi():
    data = []
    with connection.cursor() as cursor:
        cursor.execute("select kode, nama_instansi from sivax.instansi")
        data = cursor.fetchall()
    return data