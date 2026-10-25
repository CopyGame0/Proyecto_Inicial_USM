from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan_semanal, name='plan_semanal'),
    path('receta/<int:receta_id>/', views.detalle_receta, name='detalle_receta'),
]
