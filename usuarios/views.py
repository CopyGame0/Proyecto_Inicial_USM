from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('login')
    else:
        formulario = UserCreationForm()
    
    return render(request, 'usuarios/registro.html', {'formulario': formulario})