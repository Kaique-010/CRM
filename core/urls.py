from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, PedidoVendaViewSet,pedidos_por_cliente, pedidos_necessitam_contato_view, marcar_contato_realizado, detalhar_contato
from core import views
from .views import dashboard

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedidosvenda', PedidoVendaViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/pedidos', include(router.urls)),
    path('pedidos/por-cliente/', pedidos_por_cliente, name='pedidos_por_cliente'),
    path('pedidos-necessitam-contato/', pedidos_necessitam_contato_view, name='pedidos_necessitam_contato'),
    path('marcar-contato-realizado/<int:pedido_id>/', marcar_contato_realizado, name='marcar_contato_realizado'),
    path('detalhar_contato/<int:pedido_id>/', views.detalhar_contato, name='detalhar_contato'),
    path('detalhar_cliente/', detalhar_contato, name='detalhes_cliente'),
    path('dashboard/', dashboard, name='dashboard'),
]
