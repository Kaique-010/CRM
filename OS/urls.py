from django.urls import path
from .views import ordem_de_servico

urlpatterns = [
    path('os/', ordem_de_servico, name='os.html'),
]