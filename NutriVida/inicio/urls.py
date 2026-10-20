from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='home'),
    path('formulario/', views.formulario_view, name='formulario'),
]