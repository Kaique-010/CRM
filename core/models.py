from django.db import models
from entidades.models import Entidades




class Pedido(models.Model):
    cliente = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)  # Especificar max_length
    produto = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.cliente} - {self.produto}"

class PedidoVenda(models.Model):
    pedi_empr = models.IntegerField()
    pedi_fili = models.IntegerField()
    pedi_nume = models.BigAutoField(primary_key=True, unique=True)
    pedi_forn = models.ForeignKey(Entidades, on_delete=models.CASCADE, db_column='pedi_forn', related_name='pedidos_como_fornecedor')
    pedi_data = models.DateField()
    pedi_tota = models.DecimalField(decimal_places=15, max_digits=15, default=0)
    pedi_fina = models.IntegerField(default=0)
    pedi_vend = models.ForeignKey(Entidades, on_delete=models.CASCADE, db_column='pedi_vend', related_name='pedidos_como_vendedor', default= 'null')
    contato_realizado = models.BooleanField(default=False)
    data_contato = models.DateField(null=True, blank=True)
    notas_contato = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'pedidosvenda'

    def __str__(self):
        return f"Pedido {self.pedi_nume} - {self.pedi_forn}"
