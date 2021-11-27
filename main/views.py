from django.shortcuts import render


def distribusi_tugas(request):
    return render(request, 'main/home.html')
def landing_page(request):
    return render(request, 'main/landing_page.html')