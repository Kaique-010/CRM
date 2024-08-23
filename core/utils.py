from datetime import date, timedelta
from .models import PedidoVenda

def identificar_pedidos_necessitam_contato():
 
    hoje = date.today()
    dias_para_contato = 7  # Número de dias após o pedido que você deseja filtrar
    data_limite = hoje - timedelta(days=dias_para_contato)
    
    pedidos_necessitam_contato = PedidoVenda.objects.filter(
        pedi_data__lte=data_limite,
        contato_realizado=False
    )
    
    return pedidos_necessitam_contato
