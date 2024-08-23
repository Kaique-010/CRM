from django.shortcuts import render
from django.db import connection  
from core.models import Entidades
from entidades.serializers import EntidadesSerializer
from rest_framework import viewsets
from rest_framework import filters
from django.core.paginator import Paginator

# ViewSet da API
class EntidadesViewSet(viewsets.ModelViewSet):
    queryset = Entidades.objects.filter(enti_empr=1)
    serializer_class = EntidadesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def entidades_view(request):
    nome = request.GET.get('nome', '')
    id_cliente = request.GET.get('id_cliente', '')
    page_number = request.GET.get('page', 1) 

    query = """
        SELECT enti_clie,
               enti_nome,
               enti_fant,
               enti_cpf,
               enti_cnpj,
               enti_insc_esta,
               enti_cep,
               enti_ende,
               enti_nume,
               enti_cida,
               enti_esta,
               enti_fone,
               enti_celu,
               enti_emai,
               enti_emai_empr
        FROM entidades
        WHERE enti_empr = %s
    """

    params = [1]  # Empresa fixa para filtragem

    if nome:
        query += " AND enti_nome LIKE %s"
        params.append(f'%{nome}%')
    
    if id_cliente:
        query += " AND enti_clie = %s"
        params.append(id_cliente)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        entidades = dictfetchall(cursor)

    paginator = Paginator(entidades, 10)  # 20 entidades por página
    page_obj = paginator.get_page(page_number)

    context = {
        'entidades': page_obj.object_list,
        'page_obj': page_obj,
        'nome': nome,
        'id_cliente': id_cliente,
    }
    return render(request, 'entidades.html', context)