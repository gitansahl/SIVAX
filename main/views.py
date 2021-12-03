from django.shortcuts import render
from django.db import connection
from django.views.generic.base import View
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, JsonResponse

def index(request):
    return render(request, 'main/landing_page.html')

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

class DistribusiTugasView(View):
    def get(self, request):
        context = {}
        context['email'] = request.session.get('email') 
        # return email kalau ada
        context['roles'] = request.session.get('roles') 
        # return role kalau ada. contoh: ['admin', 'panitia', 'warga', 'nakes']
        return render(request, 'main/home.html', context)

    def post(self,request):
        # Ini buat logout
        try:
            del request.session['email']
            del request.session['roles']
        except:
            pass
        return HttpResponseRedirect('/trigger1/login')

def landing_page(request):
    return render(request, 'main/landing_page.html')

