#No se como funcionan los Test, asi que no voy a tocar eso XD
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path('plan/', include('recetas.urls')),
    path('formulario/', lambda request: HttpResponse("formulario"), name='formulario'),
]
