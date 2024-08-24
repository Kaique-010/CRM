from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views
from core.views import PedidoViewSet, PedidoVendaViewSet, pedidos_por_cliente, pedidos_necessitam_contato_view, marcar_contato_realizado, dashboard
from entidades.views import EntidadesViewSet, entidades_view

router_pedidos = DefaultRouter()
router_pedidos.register(r'pedidos', PedidoViewSet)
router_pedidos.register(r'pedidosvenda', PedidoVendaViewSet)

router_entidades = DefaultRouter()
router_entidades.register(r'entidades', EntidadesViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/pedidos/', include(router_pedidos.urls)),
    path('api/entidades/', include(router_entidades.urls)),
    path('core/', include('core.urls')), 
    path('entidades/', entidades_view, name='entidades.html'),  
    path('pedidos/', pedidos_por_cliente, name='pedidos_por_cliente'),  
    path('pedidos-necessitam-contato/', pedidos_necessitam_contato_view, name='pedidos_necessitam_contato'),
    path('marcar-contato-realizado/<int:pedido_id>/', marcar_contato_realizado, name='marcar_contato_realizado'),
    path('detalhar-contato/<int:pedido_id>/', views.detalhar_contato, name='detalhar_contato'),
     path('dashboard/', dashboard, name='dashboard'),
    
]
