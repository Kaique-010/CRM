from django.db import models
from entidades.models import Entidades
from produtos.models import Produtos

class OrdemServico(models.Model):
    serv_empr = models.IntegerField()  
    serv_fili = models.IntegerField()  
    serv_os = models.CharField(max_length=20)  
    os_clie = models.ForeignKey(Entidades, on_delete=models.CASCADE, related_name='ordens_servico')
    os_data_aber = models.DateField() 
    os_data_fech = models.DateField(blank=True, null=True)  
    
    class Meta:
        db_table = 'ordem_servico'  # Certifique-se de que corresponde ao nome real da tabela
        managed = False
    
    def __str__(self):
        return f"OS {self.serv_os} - {self.os_clie}"

class Servico(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='servicos')
    serv_item = models.IntegerField()
    serv_prod = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    serv_quan = models.FloatField()
    serv_unit = models.FloatField()
    serv_desc = models.FloatField()
    serv_tota = models.FloatField()

    class Meta:
        db_table = 'servicosos'  
        managed = False
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        unique_together = ('ordem_servico', 'serv_item')

    def __str__(self):
        return f"Servico {self.serv_item} - {self.serv_prod}"

class Pecaso(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='pecasos')
    peca_item = models.IntegerField()
    peca_prod = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    peca_quan = models.FloatField()
    peca_unit = models.FloatField()
    peca_desc = models.FloatField()
    peca_tota = models.FloatField()

    class Meta:
        db_table = 'pecasos'  
        managed = False
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        unique_together = ('ordem_servico', 'peca_item')

    def __str__(self):
        return f"Pecaso {self.peca_item} - {self.peca_prod}"
