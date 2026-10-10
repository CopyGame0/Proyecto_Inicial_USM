from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Perfil

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm 
    model = Perfil
    
    # Columnas que se mostrarán en la lista del admin 
    list_display = ['username', 'email', 'pauta_nutricional', 'is_staff']
    
admin.site.register(Perfil, CustomUserAdmin)