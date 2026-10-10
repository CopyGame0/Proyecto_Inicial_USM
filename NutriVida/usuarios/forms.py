from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import Perfil

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Perfil
        fields = ('username', 'email', 'pauta_nutricional', 'edad')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta():
        model = Perfil
        fields = ('username', 'email', 'pauta_nutricional', 'edad')
                