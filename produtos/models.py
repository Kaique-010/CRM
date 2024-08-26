from django.db import models

class GrupoProduto(models.Model):
    codigo = models.CharField(max_length=50, db_column='grup_codi', primary_key=True)
    descricao = models.CharField(max_length=255, db_column='grup_desc')

    class Meta:
        db_table = 'gruposprodutos'
        managed = False

    def __str__(self):
        return self.descricao

class SubgrupoProduto(models.Model):
    codigo = models.CharField(max_length=50, db_column='sugr_codi', primary_key=True)
    descricao = models.CharField(max_length=255, db_column='sugr_desc')

    class Meta:
        db_table = 'subgruposprodutos'
        managed = False

    def __str__(self):
        return self.descricao

class FamiliaProduto(models.Model):
    codigo = models.CharField(max_length=50, db_column='fami_codi', primary_key=True)
    descricao = models.CharField(max_length=255, db_column='fami_desc')

    class Meta:
        db_table = 'familiaprodutos'
        managed = False

    def __str__(self):
        return self.descricao

class Marca(models.Model):
    codigo = models.CharField(max_length=50, db_column='marc_codi', primary_key=True)
    nome = models.CharField(max_length=255, db_column='marc_nome')

    class Meta:
        db_table = 'marca'
        managed = False

    def __str__(self):
        return self.nome

class TabelaPrecos(models.Model):
    produto_codigo = models.CharField(max_length=50, db_column='tabe_prod', unique=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, db_column='tabe_cuge')
    preco_a_vista = models.DecimalField(max_digits=10, decimal_places=2, db_column='tabe_avis')
    preco_a_prazo = models.DecimalField(max_digits=10, decimal_places=2, db_column='tabe_apra')

    class Meta:
        db_table = 'tabelaprecos'
        managed = False

class SaldoProduto(models.Model):
    produto_codigo = models.CharField(max_length=50, db_column='sapr_prod', unique=True)
    empresa = models.CharField(max_length=50, db_column='sapr_empr')
    filial = models.CharField(max_length=50, db_column='sapr_fili')
    saldo_estoque = models.DecimalField(max_digits=10, decimal_places=2, db_column='sapr_sald')

    class Meta:
        db_table = 'saldosprodutos'
        managed = False

class Produtos(models.Model):
    produto_codigo = models.CharField(max_length=50, db_column='prod_codi', primary_key=True)
    nome_produto = models.CharField(max_length=255, db_column='prod_nome')
    unidade_medida = models.CharField(max_length=10, db_column='prod_unme')
    grupo = models.ForeignKey(GrupoProduto, on_delete=models.DO_NOTHING, db_column='prod_grup', related_name='produtos')
    subgrupo = models.ForeignKey(SubgrupoProduto, on_delete=models.DO_NOTHING, db_column='prod_sugr', related_name='produtos')
    familia = models.ForeignKey(FamiliaProduto, on_delete=models.DO_NOTHING, db_column='prod_fami', related_name='produtos')
    local = models.CharField(max_length=255, db_column='prod_loca')
    ncm = models.CharField(max_length=10, db_column='prod_ncm')
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, db_column='prod_marc', related_name='produtos')
    codigo_fabricante = models.CharField(max_length=50, db_column='prod_codi_fabr')
    foto = models.ImageField(upload_to='fotos/', db_column='prod_foto', blank=True, null=True)

   

    class Meta:
        db_table = 'produtos'
        managed = False
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.nome_produto} ({self.produto_codigo})'