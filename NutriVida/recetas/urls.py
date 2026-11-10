from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan_semanal, name='plan_semanal'),
    path('receta/<int:receta_id>/', views.detalle_receta, name='detalle_receta'),
 
    # Ruta para abrir la lista de compras en una nueva pestaña
    path('receta/<int:receta_id>/supermercados/', views.supermercados_receta, name='supermercados_receta'),
]
