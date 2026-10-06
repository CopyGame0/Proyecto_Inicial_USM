from django.shortcuts import render

# Create your views here.
from django.http import Httpresponse
def pagina_principal(request):
    return Httpresponse("<h1>Bienvenido a NutriVida</h1>")
