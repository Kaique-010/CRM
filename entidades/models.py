from django.db import models

class Entidades(models.Model):
    enti_empr = models.IntegerField(default=1)
    enti_clie = models.IntegerField(default=0, primary_key=True)  
    enti_nome = models.CharField(max_length=100, default='UNKNOWN')
    enti_fant = models.CharField(max_length=100, default='UNKNOWN')  
    enti_cpf = models.CharField(max_length=11, default='00000000000')  
    enti_cnpj = models.CharField(max_length=14, default='00000000000000')  
    enti_insc_esta = models.CharField(max_length=11, default='00000000000')  
    enti_cep = models.CharField(max_length=8, default='00000000') 
    enti_ende = models.CharField(max_length=60, default='UNKNOWN')
    enti_nume = models.CharField(max_length=4, default='0000')  
    enti_cida = models.CharField(max_length=60, default='UNKNOWN')
    enti_esta = models.CharField(max_length=2, default='PR')
    enti_fone = models.CharField(max_length=14, default='00000000000') 
    enti_celu = models.CharField(max_length=15, default='UNKNOWN')
    enti_emai = models.CharField(max_length=60, default='UNKNOWN')
    enti_emai_empr = models.CharField(max_length=60, default='UNKNOWN')


    def __str__(self):
        return self.enti_nome

    class Meta:
        db_table = 'entidades'