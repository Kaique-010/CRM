from datetime import date, timedelta
import json
import csv
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import viewsets
from .models import Pedido, PedidoVenda
from .serializers import PedidoSerializer, PedidoVendaSerializer
from django.db import connection
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned

def dictfetchall(cursor):
    """Converte o resultado do cursor em uma lista de dicionários."""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def home(request):
    nome_cliente = request.GET.get('nome_cliente', '')
    cpf = request.GET.get('cpf', '')
    status = request.GET.get('status', '')

    query = """
        SELECT DISTINCT
            "Empresa",
            "Filial",
            "Cliente",
            "Nome_Cliente",
            "CPF",
            "CNPJ",
            "Cidade",
            "Estado",
            "Titulo",
            "Parcelas",
            "Série",
            "Emissão",
            "Vencimento",
            "Valor",
            "Titulo_Pago",
            "Valor_Pago",
            "Saldo_a_Receber",
            CASE
                WHEN "Stat_recebimento" = 'A' THEN 'A- Aberto'
                WHEN "Stat_recebimento" = 'P' THEN 'P- Parcial'
                WHEN "Stat_recebimento" = 'T' THEN 'T- Total'
                ELSE 'Desconhecido'
            END AS "Stat_recebimento",
            CASE
                WHEN "Status" = 'A' THEN 'A- Aberto'
                WHEN "Status" = 'P' THEN 'P- Parcial'
                WHEN "Status" = 'T' THEN 'T- Total'
                ELSE 'Desconhecido'
            END AS "Status"
        FROM (
            SELECT 
                tr.titu_empr AS "Empresa",
                tr.titu_fili AS "Filial",
                tr.titu_clie AS "Cliente",
                enti.enti_nome AS "Nome_Cliente",
                enti.enti_cpf AS "CPF",
                enti.enti_cnpj AS "CNPJ",
                enti.enti_cida AS "Cidade",
                enti.enti_esta AS "Estado",
                tr.titu_titu AS "Titulo",
                tr.titu_parc AS "Parcelas",
                tr.titu_seri AS "Série",
                tr.titu_emis AS "Emissão",
                tr.titu_venc AS "Vencimento",
                tr.titu_valo AS "Valor",
                bare.bare_titu AS "Titulo_Pago",
                bare.bare_pago AS "Valor_Pago",
                bare.bare_topa AS "Stat_recebimento",
                tr.titu_aber AS "Status",
                (tr.titu_valo - COALESCE(bare.bare_pago, 0)) AS "Saldo_a_Receber"
            FROM
                titulosreceber AS tr
            LEFT JOIN
                entidades AS enti ON tr.titu_clie = enti.enti_clie
            LEFT JOIN
                baretitulos AS bare ON tr.titu_titu = bare.bare_titu
            WHERE 1=1
    """

    params = []

    if nome_cliente:
        query += " AND enti.enti_nome LIKE %s"
        params.append(f'%{nome_cliente}%')
    
    if cpf:
        query += " AND enti.enti_cpf = %s"
        params.append(cpf)
    
    if status:
        query += " AND (bare.bare_topa = %s OR tr.titu_aber = %s)"
        params.append(status)
        params.append(status)

    query += " ORDER BY \"Nome_Cliente\" ASC"
    query += ") AS subquery"

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        crm_data = dictfetchall(cursor)

    paginator = Paginator(crm_data, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'nome_cliente': nome_cliente,
        'cpf': cpf,
        'status': status,
    }

    return render(request, 'home.html', context)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoVendaViewSet(viewsets.ModelViewSet):
    queryset = PedidoVenda.objects.all()
    serializer_class = PedidoVendaSerializer

def pedidos_por_cliente(request):
    nome_cliente = request.GET.get('nome_cliente', '')
    num_pedido = request.GET.get('num_pedido', '')
    page_number = request.GET.get('page', 1) 

    query = """
        SELECT
            p.pedi_empr,
            p.pedi_fili,
            e.enti_nome,
            COUNT(DISTINCT p.pedi_nume) AS total_pedidos,
            ARRAY_AGG(p.pedi_data) AS datas_pedidos,
            SUM(p.pedi_tota) AS total_valor_pedidos,
            CASE 
                WHEN MAX(p.pedi_fina) = 0 THEN 'À vista'
                WHEN MAX(p.pedi_fina) = 1 THEN 'A prazo'
                WHEN MAX(p.pedi_fina) = 2 THEN 'Sem Financeiro'
                WHEN MAX(p.pedi_fina) = 3 THEN 'Na NF'
                WHEN MAX(p.pedi_fina) = 4 THEN 'Troca'
                ELSE 'Outro'
            END AS tipo_financeiro
        FROM pedidosvenda p
        LEFT JOIN entidades e ON p.pedi_forn = e.enti_clie AND p.pedi_empr = e.enti_empr
        WHERE 1=1
    """
    
    params = []

    if nome_cliente:
        query += " AND e.enti_nome LIKE %s"
        params.append(f'%{nome_cliente}%')
    
    if num_pedido:
        query += " AND p.pedi_nume = %s"
        params.append(num_pedido)

    query += """
        GROUP BY p.pedi_empr, p.pedi_fili, e.enti_nome, p.pedi_tota
        ORDER BY total_pedidos DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        all_clientes_pedidos = dictfetchall(cursor)

    paginator = Paginator(all_clientes_pedidos, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'clientes_pedidos': page_obj,
        'nome_cliente': nome_cliente,
        'num_pedido': num_pedido,
        'page_obj': page_obj,
    }

    return render(request, 'pedidos_por_cliente.html', context)

def pedidos_necessitam_contato_view(request):
    hoje = date.today()
    dias_para_contato = 7  
    data_limite = hoje - timedelta(days=dias_para_contato)
    
    # Captura os filtros da requisição GET
    filtro_vendedor = request.GET.get('vendedor')
    filtro_pedido = request.GET.get('pedido_id')
    filtro_cliente = request.GET.get('cliente')

    # Ajusta a consulta SQL com base nos filtros
    query = """
        WITH UltimosPedidos AS (
            SELECT
                p.pedi_nume,
                e.enti_nome AS cliente,
                p.pedi_data,
                p.notas_contato,
                v.enti_nome AS vendedor,
                ROW_NUMBER() OVER (PARTITION BY e.enti_nome ORDER BY p.pedi_data DESC) AS rn
            FROM pedidosvenda p
            LEFT JOIN entidades e ON p.pedi_forn = e.enti_clie AND p.pedi_empr = e.enti_empr
            LEFT JOIN entidades v ON p.pedi_vend = v.enti_clie AND p.pedi_empr = v.enti_empr
        )
        SELECT
            pedi_nume,
            cliente,
            pedi_data,
            notas_contato,
            vendedor
        FROM UltimosPedidos
        WHERE rn = 1
        AND pedi_data <= %s
    """

    # Lista de parâmetros para a consulta
    params = [data_limite]

    # Aplica os filtros opcionais
    if filtro_vendedor:
        query += " AND vendedor = %s"
        params.append(filtro_vendedor)
    if filtro_pedido:
        query += " AND pedi_nume = %s"
        params.append(filtro_pedido)
    if filtro_cliente:
        query += " AND cliente = %s"
        params.append(filtro_cliente)

    query += " ORDER BY pedi_data ASC;"

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        pedidos_necessitam_contato = dictfetchall(cursor)

    # Paginação
    paginator = Paginator(pedidos_necessitam_contato, 10)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    context = {
        'pedidos_necessitam_contato': page_obj,
        'filtro_vendedor': filtro_vendedor,
        'filtro_pedido': filtro_pedido,
        'filtro_cliente': filtro_cliente,
    }

    return render(request, 'pedidos_necessitam_contato.html', context)

def marcar_contato_realizado(request, pedido_id):
    try:
        pedido = PedidoVenda.objects.get(pedi_nume=pedido_id)
        pedido.contato_realizado = True
        pedido.data_contato = date.today()
        pedido.save()
    except PedidoVenda.DoesNotExist:
        return redirect('pedidos_necessitam_contato')
    except MultipleObjectsReturned:
        return redirect('pedidos_necessitam_contato')

    return redirect('detalhar_contato', pedido_id=pedido_id)

def detalhar_contato(request, pedido_id):
    query = """
        SELECT
            p.pedi_nume,
            e.enti_nome,
            e.enti_fone,
            e.enti_emai,
            e.enti_emai_empr,
            p.pedi_data,
            p.notas_contato
        FROM pedidosvenda p
        LEFT JOIN entidades e ON p.pedi_forn = e.enti_clie AND p.pedi_empr = e.enti_empr
        WHERE p.pedi_nume = %s
    """
    
    params = [pedido_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultado = dictfetchall(cursor)

    if not resultado:
        raise Http404("Pedido não encontrado")

    pedido = resultado[0]

    if request.method == 'POST':
        notas = request.POST.get('notas')
        update_query = """
            UPDATE pedidosvenda
            SET notas_contato = %s
            WHERE pedi_nume = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(update_query, [notas, pedido_id])
        
        return redirect('pedidos_necessitam_contato')

    context = {
        'pedido': pedido,
    }

    return render(request, 'detalhar_contato.html', context)

def detalhar_cliente(request, pedido_id):
    query = """
        SELECT
            p.pedi_nume AS "Pedido",
            e.enti_nome AS "Nome Cliente",
            e.enti_fone AS "Telefone",
            e.enti_emai AS "Email1",
            e.enti_emai_empr AS "Email2",
            p.pedi_data AS "Data do Pedido",
            p.notas_contato AS "Notas"
        FROM pedidosvenda p
        LEFT JOIN entidades e ON p.pedi_forn = e.enti_clie AND p.pedi_empr = e.enti_empr
        WHERE p.pedi_nume = %s
    """
    
    params = [pedido_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultado = dictfetchall(cursor)

    if not resultado:
        raise Http404("Pedido não encontrado")

    contato = resultado[0]

    if request.method == 'POST':
        notas = request.POST.get('notas')
        update_query = """
            UPDATE pedidosvenda
            SET notas_contato = %s
            WHERE pedi_nume = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(update_query, [notas, pedido_id])
        
        return redirect('crm_home')

    context = {
        'contato': contato,
    }

    return render(request, 'detalhar_cliente.html', context)


def dictfetchall(cursor):
    """Converte todas as linhas do cursor em um dicionário."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dashboard(request):

    vendedor = request.GET.get('vendedor', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Obter lista de vendedores
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT e1.enti_clie, e1.enti_nome
            FROM pedidosvenda p
            LEFT JOIN entidades e1 ON p.pedi_vend = e1.enti_clie AND p.pedi_empr = e1.enti_empr
            WHERE p.pedi_canc = false
            ORDER BY e1.enti_nome ASC;
        """)
        vendedores = cursor.fetchall()
        vendedores_list = [{'id': vendedor[0], 'nome': vendedor[1]} for vendedor in vendedores]

    # Consulta principal
    query = """
        SELECT 
            MAX(p.pedi_vend) AS "COD VENDEDOR",
            MAX(e1.enti_nome) AS "Nome Vendedor",
            COUNT(DISTINCT i.iped_pedi) AS "Total Pedidos",
            SUM(i.iped_tota) AS "Total Valor dos Pedidos"
        FROM 
            itenspedidovenda i
        LEFT JOIN 
            pedidosvenda p ON i.iped_pedi = p.pedi_nume AND i.iped_empr = p.pedi_empr AND i.iped_fili = p.pedi_fili
        LEFT JOIN 
            entidades e1 ON p.pedi_vend = e1.enti_clie AND p.pedi_empr = e1.enti_empr
        WHERE 
            p.pedi_canc = false
    """

    params = []
    if vendedor:
        query += " AND e1.enti_clie = %s"
        params.append(vendedor)
    
    if data_inicio:
        query += " AND i.iped_data >= %s"
        params.append(data_inicio)

    if data_fim:
        query += " AND i.iped_data <= %s"
        params.append(data_fim)
    
    query += """
        GROUP BY 
            p.pedi_vend, e1.enti_nome
        ORDER BY 
            e1.enti_nome ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = dictfetchall(cursor)

    # Prepare data for the chart
    labels = [item['Nome Vendedor'] for item in data]
    total_pedidos = [float(item['Total Pedidos']) for item in data]
    total_valor_pedido = [float(item['Total Valor dos Pedidos']) for item in data]

    context = {
        'labels': json.dumps(labels),
        'total_pedidos': json.dumps(total_pedidos),
        'total_valor_pedido': json.dumps(total_valor_pedido),
        'vendedor': vendedor,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'vendedores': vendedores_list
    }

    return render(request, 'dashboard.html', context)


