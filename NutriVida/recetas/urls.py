from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan_semanal, name='plan_semanal'),
]
