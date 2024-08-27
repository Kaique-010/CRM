from django.db import connection
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from core.views import dictfetchall
from OS.models import OrdemServico
from OS.serializers import OSSerializers
from rest_framework import viewsets, filters

# ViewSet da API
class OSViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()  # Ajustado para refletir a filtragem real
    serializer_class = OSSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['serv_os']  # Ajuste o campo conforme o seu modelo

def ordem_de_servico(request):
    nome = request.GET.get('nome', '')
    id_prod = request.GET.get('id_prod', '')
    page_number = request.GET.get('page', 1)

    # Montagem da query SQL com filtros
    query = """
    SELECT * FROM (
    (SELECT serv_empr AS Empresa, 
            serv_fili AS Filial,
            os_data_aber AS "Abertura",
            os_data_fech AS "Fechamento",
            serv_os AS "O.S",
            os_clie AS "Cliente",
            enti_nome AS "Nome Cliente",
            serv_item AS Item,
            serv_prod AS Produto, 
            'Serviço' AS Tipo, 
            prod_nome AS Nome,      
            serv_quan AS Quantidade,
            serv_unit AS Unitário,
            serv_desc AS Desconto,
            serv_tota AS Total,
            CASE 
                WHEN os_stat_os = 0 THEN 'Aberta'
                WHEN os_stat_os = 1 THEN 'Parcial'
                WHEN os_stat_os = 2 THEN 'Faturada'
                WHEN os_stat_os = 3 THEN 'Cancelada'
                ELSE 'Desconhecido'
            END AS "Status"
    FROM servicosos 
    LEFT JOIN produtos ON prod_codi = serv_prod AND prod_empr = serv_empr 
    INNER JOIN os ON serv_os = os_os AND serv_empr = os_empr AND serv_fili = os_fili
    LEFT JOIN entidades ON os_clie = entidades.enti_clie::integer AND serv_empr = enti_empr
    WHERE (prod_nome ILIKE %s OR %s = '') AND (%s = '' OR serv_prod::text = %s))
    
    UNION ALL
    
    (SELECT peca_empr AS Empresa,
            peca_fili AS Filial,
            os_data_aber AS "Abertura",
            os_data_fech AS "Fechamento",
            peca_os AS "O.S",
            os_clie AS "Cliente",
            enti_nome AS "Nome Cliente",
            peca_item,
            peca_prod AS Produto,
            'Produto' AS Tipo, 
            prod_nome AS Nome,       
            peca_quan AS Quantidade,
            peca_unit AS Unitário,
            peca_desc AS Desconto,
            peca_tota AS Total,
            CASE 
                WHEN os_stat_os = 0 THEN 'Aberta'
                WHEN os_stat_os = 1 THEN 'Parcial'
                WHEN os_stat_os = 2 THEN 'Faturada'
                WHEN os_stat_os = 3 THEN 'Cancelada'
                ELSE 'Desconhecido'
            END AS "Status"
    FROM pecasos 
    LEFT JOIN produtos ON prod_codi = peca_prod AND prod_empr = peca_empr 
    INNER JOIN os ON peca_os = os_os AND peca_empr = os_empr AND peca_fili = os_fili
    LEFT JOIN entidades ON os_clie = entidades.enti_clie::integer AND os_empr = enti_empr
    WHERE (prod_nome ILIKE %s OR %s = '') AND (%s = '' OR peca_prod::text = %s))
) AS x
ORDER BY 
     Empresa,
     "O.S",
     Item;
    """
    params = [f'%{nome}%', nome, id_prod, id_prod, f'%{nome}%', nome, id_prod, id_prod]

    # Executar a consulta SQL
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        ordens = dictfetchall(cursor)

    # Paginação
    paginator = Paginator(ordens, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'os.html', {
        'page_obj': page_obj,
        'nome': nome,
        'id_prod': id_prod
    })
