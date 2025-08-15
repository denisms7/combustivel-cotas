import pandas as pd
from django.shortcuts import render
from django.utils.dateparse import parse_date
from controle.models import Abastecimento
from datetime import datetime, timedelta, date

def relatorio_abastecimento(request):
    hoje = date.today()

    # Pega as datas passadas via GET ou usa padrão
    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')

    if data_inicial_str:
        data_inicial = parse_date(data_inicial_str)
    else:
        data_inicial = hoje.replace(day=1)  # Primeiro dia do mês

    if data_final_str:
        data_final = parse_date(data_final_str)
    else:
        data_final = hoje  # Hoje

    # Ajusta para considerar o dia todo
    data_inicial = datetime.combine(data_inicial, datetime.min.time())
    data_final = datetime.combine(data_final, datetime.max.time())

    # Base queryset
    qs = Abastecimento.objects.select_related('secretaria', 'veiculo', 'veiculo__cota')
    qs = qs.filter(cadastrado_em__range=[data_inicial, data_final])

    if not qs.exists():
        return render(request, 'relatorios/rel_abastecimento.html', {
            'litros_por_secretaria_combustivel': [],
            'litros_por_carro': [],
            'data_inicial': data_inicial.date(),
            'data_final': data_final.date(),
        })

    registros = []
    for ab in qs:
        litros = ab.veiculo.cota.litros  # <-- pega o valor realmente abastecido
        registros.append({
            'secretaria': ab.secretaria.secretaria,
            'combustivel': ab.veiculo.get_combustivel_display(),
            'descricao': ab.veiculo.descricao,
            'placa': ab.veiculo.placa or '',
            'litros': litros,
        })

    df = pd.DataFrame(registros)

    df_secretaria = (
        df.groupby(['secretaria', 'combustivel'], as_index=False)['litros']
        .sum()
        .rename(columns={'litros': 'total_litros'})
        .sort_values(by=['secretaria', 'combustivel'])
    )

    df_carro = (
        df.groupby(['placa', 'descricao', 'combustivel'], as_index=False)['litros']
        .sum()
        .rename(columns={'litros': 'total_litros'})
        .sort_values(by=['placa', 'descricao', 'combustivel'])
    )

    contexto = {
        'litros_por_secretaria_combustivel': df_secretaria.to_dict(orient='records'),
        'litros_por_carro': df_carro.to_dict(orient='records'),
        'data_inicial': data_inicial.date(),
        'data_final': data_final.date(),
    }

    return render(request, 'relatorios/rel_abastecimento.html', contexto)
