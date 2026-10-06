from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def pagina_principal(request):
    return HttpResponse("<h>Bienvenido a NutriVida</h1>")
