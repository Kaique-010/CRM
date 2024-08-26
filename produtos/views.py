from datetime import date, timedelta
import json
import csv
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import viewsets
from produtos.serializers import ProdutosSerializers
from .models import Produtos
from django.db import connection
from django.core.paginator import Paginator

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializers
    filterset_fields = ['nome', 'id_produto']
    search_fields = ['nome', 'codigo_produto']


def produtos_view(request):
    nome = request.GET.get('nome', '')
    id_prod = request.GET.get('id_prod', '')
    page_number = request.GET.get('page', 1) 

    # Montagem da query SQL
    query = """
    SELECT DISTINCT 
        s.sapr_empr AS "Empresa",
        s.sapr_fili AS "Filial",
        p.prod_codi AS "codigo_produto",
        p.prod_nome AS "nome_produto",
        p.prod_unme AS "unidade_medida",
        p.prod_grup AS "codigo_grupo",
        gp.grup_desc AS "descricao_grupo",
        p.prod_sugr AS "codigo_subgrupo",
        sp.sugr_desc AS "descricao_subgrupo",
        p.prod_fami AS "codigo_familia",
        fp.fami_desc AS "descricao_familia",
        p.prod_loca AS "Local",
        p.prod_ncm AS "ncm",
        p.prod_marc AS "codigo_marca",
        p.prod_foto AS "foto",
        m.marc_nome AS "nome_marca",
        p.prod_codi_fabr AS "codigo_fabricante",
        t.tabe_cuge AS "preco_custo",
        t.tabe_avis AS "preco_a_vista",
        t.tabe_apra AS "preco_a_prazo",
        s.sapr_sald AS "saldo_estoque"
    FROM 
        produtos p
    LEFT JOIN 
        tabelaprecos t ON p.prod_codi::text = t.tabe_prod::text
    LEFT JOIN 
        gruposprodutos gp ON p.prod_grup::text = gp.grup_codi::text
    LEFT JOIN 
        subgruposprodutos sp ON p.prod_sugr::text = sp.sugr_codi::text
    LEFT JOIN 
        familiaprodutos fp ON p.prod_fami::text = fp.fami_codi::text
    LEFT JOIN 
        saldosprodutos s ON p.prod_codi::text = s.sapr_prod::text
    LEFT JOIN 
        marca m ON p.prod_marc = m.marc_codi
    WHERE 
        s.sapr_sald > 0
        AND p.prod_empr = 5
        AND s.sapr_fili >= 0
    """


    # Aplicar filtros se necessário
    if nome:
        query += " AND p.prod_nome ILIKE %s"
    if id_prod:
        query += " AND p.prod_codi = %s"

    # Parâmetros para os filtros
    params = []
    if nome:
        params.append(f"%{nome}%")
    if id_prod:
        params.append(id_prod)

    # Executar a consulta SQL
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        produtos = dictfetchall(cursor)

    # Paginação
    paginator = Paginator(produtos, 10) 
    page_obj = paginator.get_page(page_number)

    return render(request, 'produtos_lista.html', {'page_obj': page_obj, 'nome': nome, 'id_prod': id_prod})


def dictfetchall(cursor):
    "Converte os resultados da consulta para uma lista de dicionários."
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def exportar_produtos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Código Produto', 'Nome', 'Unidade Medida', 'Código Grupo', 'Descrição Grupo', 
        'Código Subgrupo', 'Descrição Subgrupo', 'Código Família', 'Descrição Família', 
        'Local', 'NCM', 'Código Marca', 'Nome Marca', 'Código Fabricante', 
        'Preço Custo', 'Preço à Vista', 'Preço a Prazo', 'Saldo Estoque'
    ])

    # Montagem da query SQL
    query = """
    SELECT DISTINCT 
        s.sapr_empr AS "Empresa",
        s.sapr_fili AS "Filial",
        p.prod_codi AS "codigo_produto",
        p.prod_nome AS "nome_produto",
        p.prod_unme AS "unidade_medida",
        p.prod_grup AS "codigo_grupo",
        gp.grup_desc AS "descricao_grupo",
        p.prod_sugr AS "codigo_subgrupo",
        sp.sugr_desc AS "descricao_subgrupo",
        p.prod_fami AS "codigo_familia",
        fp.fami_desc AS "descricao_familia",
        p.prod_loca AS "local",
        p.prod_ncm AS "ncm",
        p.prod_marc AS "codigo_marca",
        p.prod_foto AS "foto",
        m.marc_nome AS "nome_marca",
        p.prod_codi_fabr AS "codigo_fabricante",
        t.tabe_cuge AS "preco_custo",
        t.tabe_avis AS "preco_a_vista",
        t.tabe_apra AS "preco_a_prazo",
        s.sapr_sald AS "saldo_estoque"
    FROM 
        produtos p
    LEFT JOIN 
        tabelaprecos t ON p.prod_codi::text = t.tabe_prod::text
    LEFT JOIN 
        gruposprodutos gp ON p.prod_grup::text = gp.grup_codi::text
    LEFT JOIN 
        subgruposprodutos sp ON p.prod_sugr::text = sp.sugr_codi::text
    LEFT JOIN 
        familiaprodutos fp ON p.prod_fami::text = fp.fami_codi::text
    LEFT JOIN 
        saldosprodutos s ON p.prod_codi::text = s.sapr_prod::text
    LEFT JOIN 
        marca m ON p.prod_marc = m.marc_codi
    WHERE 
        s.sapr_sald > 0
        AND p.prod_empr = 5
        AND s.sapr_fili >= 0
    """


    with connection.cursor() as cursor:
        cursor.execute(query)
        produtos = dictfetchall(cursor)

   
    if produtos:
        print("Colunas disponíveis:", produtos[0].keys())

 
    for produto in produtos:
        writer.writerow([
            produto.get('codigo_produto', ''),
            produto.get('nome_produto', ''),
            produto.get('unidade_medida', ''),
            produto.get('codigo_grupo', ''),
            produto.get('descricao_grupo', ''),
            produto.get('codigo_subgrupo', ''),
            produto.get('descricao_subgrupo', ''),
            produto.get('codigo_familia', ''),
            produto.get('descricao_familia', ''),
            produto.get('local', ''),  
            produto.get('ncm', ''),
            produto.get('codigo_marca', ''),
            produto.get('nome_marca', ''),
            produto.get('codigo_fabricante', ''),
            produto.get('preco_custo', ''),
            produto.get('preco_a_vista', ''),
            produto.get('preco_a_prazo', ''),
            produto.get('saldo_estoque', '')
        ])

    return response

def dictfetchall(cursor):
    "Converte os resultados da consulta para uma lista de dicionários."
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]