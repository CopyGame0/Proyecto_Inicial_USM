from django.shortcuts import render
from django.contrib import messages
from .forms import CustomUserCreationForm

def registrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'¡Cuenta creada exitosamente para {usuario.username}!')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})