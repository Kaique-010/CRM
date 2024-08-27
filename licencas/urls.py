from django.urls import path
from .views import listar_licencas

urlpatterns = [
    path('licencas/', listar_licencas, name='listar_licencas'),
]
