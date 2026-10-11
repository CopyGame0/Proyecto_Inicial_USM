from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Usuario

from django.contrib.auth.forms import AdminUserCreationForm

class CustomAdminCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'edad', 'pauta_nutricional')

class CustomUserAdmin(UserAdmin):
    add_form = CustomAdminCreationForm      # admin gets the Admin form...
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'edad', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (('Datos nutricionales', {'fields': ('edad', 'pauta_nutricional')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Datos nutricionales', {'fields': ('email', 'edad', 'pauta_nutricional')}),)