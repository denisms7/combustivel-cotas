import pandas as pd
from django.shortcuts import render
from django.utils.dateparse import parse_date
from controle.models import Abastecimento


def relatorio_abastecimento(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    # Converte datas
    if data_inicial:
        data_inicial = parse_date(data_inicial)
    if data_final:
        data_final = parse_date(data_final)

    # Base queryset filtrado
    qs = Abastecimento.objects.select_related('secretaria', 'veiculo', 'veiculo__cota')

    if data_inicial:
        qs = qs.filter(cadastrado_em__gte=data_inicial)
    if data_final:
        qs = qs.filter(cadastrado_em__lte=data_final)

    # Se não houver registros, evitar erro no pandas
    if not qs.exists():
        return render(request, 'relatorios/rel_abastecimento.html', {
            'litros_por_secretaria_combustivel': [],
            'litros_por_carro': [],
            'data_inicial': data_inicial,
            'data_final': data_final,
        })

    # Converte queryset para DataFrame e calcula litros
    registros = []
    for ab in qs:
        litros = ab.veiculo.cota.litros * ab.veiculo.cota_qnt
        registros.append({
            'secretaria': ab.secretaria.secretaria,
            'combustivel': ab.veiculo.get_combustivel_display(),
            'placa': ab.veiculo.placa or '',
            'litros': litros,
        })

    df = pd.DataFrame(registros)

    # 1️⃣ Agrupar por Secretaria e Tipo de Combustível
    df_secretaria = (
        df.groupby(['secretaria', 'combustivel'])['litros']
        .sum()
        .reset_index()
        .rename(columns={'litros': 'total_litros'})
    )

    # 2️⃣ Agrupar por Carro
    df_carro = (
        df.groupby(['placa'])['litros']
        .sum()
        .reset_index()
        .rename(columns={'litros': 'total_litros'})
    )

    contexto = {
        'litros_por_secretaria_combustivel': df_secretaria.to_dict(orient='records'),
        'litros_por_carro': df_carro.to_dict(orient='records'),
        'data_inicial': data_inicial,
        'data_final': data_final,
    }

    return render(request, 'relatorios/rel_abastecimento.html', contexto)




