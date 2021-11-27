from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'register.html')
def register_warga(request):
    return render(request, 'register_warga.html')
def register_admin(request):
    return render(request, 'register_admin.html')
def register_panitia(request):
    return render(request, 'register_panitia.html')
