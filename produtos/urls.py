from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutosViewSet, ProdutosSerializers,produtos_view, exportar_produtos

# Cria um router para o EntidadesViewSet
router = DefaultRouter()
router.register(r'produtos', ProdutosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('produtos_lista', produtos_view, name='produtos_lista.html'),
    path('exportar-produtos/',exportar_produtos, name='exportar_produtos')
  
]
