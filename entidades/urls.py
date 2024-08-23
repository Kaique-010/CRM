from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntidadesViewSet, Entidades

# Cria um router para o EntidadesViewSet
router = DefaultRouter()
router.register(r'entidades', EntidadesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lista', Entidades, name='entidades.html' )
]
