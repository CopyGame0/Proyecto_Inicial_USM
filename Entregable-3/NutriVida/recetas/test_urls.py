"""URLs mínimas SOLO para los tests (así no dependen de la app 'inicio')."""
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path('plan/', include('recetas.urls')),
    path('formulario/', lambda request: HttpResponse("formulario"), name='formulario'),
]
