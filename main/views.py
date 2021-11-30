from django.shortcuts import render
from django.db import connection

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

def distribusi_tugas(request):
    return render(request, 'main/home.html')
def landing_page(request):
    return render(request, 'main/landing_page.html')

def index(request):
    print(request)
    # print(request.session)
    with connection.cursor() as cursor:
        cursor.execute("select * from sivax.test")
        row = cursor.fetchall()
    print(row)
    return render(request, 'main/landing_page.html')
