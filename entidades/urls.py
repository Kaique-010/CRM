from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntidadesViewSet, Entidades
from entidades.views import exportar_csv

# Cria um router para o EntidadesViewSet
router = DefaultRouter()
router.register(r'entidades', EntidadesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lista', Entidades, name='entidades.html'),
    path('exportar-csv/',exportar_csv, name='exportar_csv')
]
