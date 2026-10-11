from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'pauta_nutricional', 'edad')
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'pauta_nutricional', 'edad')
                