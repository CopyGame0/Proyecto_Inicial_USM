from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Cuenta creada exitosamente para {usuario.username}!')
            return redirect('home') 
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})