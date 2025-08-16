from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Veiculo, Cota, Secretaria
from django.conf import settings
import os
import pandas as pd


@receiver(post_migrate)
def cadastrar_cotas_padrao(sender, **kwargs):
    if sender.name != 'controle': 
        return

    cotas_padrao = [
        {'nome': 'Cota Semanal A', 'litros': 20, 'tipo': 1},
        {'nome': 'Cota Semanal B', 'litros': 10, 'tipo': 1},
    ]

    for cota_data in cotas_padrao:
        obj, criado = Cota.objects.get_or_create(
            nome=cota_data['nome'],
            defaults={
                'litros': cota_data['litros'],
                'tipo': cota_data['tipo'],
            }
        )
        if criado:
            print(f'Cota criada: {obj.nome}')


@receiver(post_migrate)
def cadastrar_secretarias_padrao(sender, **kwargs):
    if sender.name != 'controle': 
        return
    
    secretarias_padrao = [
        "Chefia de Gabinete", 
        "Procuradoria Geral", 
        "Controladoria", 
        "Secretaria de Administração", 
        "Secretaria de Fazenda", 
        "Secretaria de Planejamento e Gestão", 
        "Secretaria de Desenvolvimento Econômico e Turismo", 
        "Secretaria de Agricultura e Meio Ambiente", 
        "Secretaria de Saúde", 
        "Secretaria de Educação", 
        "Secretaria de Esporte, Cultura e Lazer", 
        "Secretaria de Assistência Social", 
        "Secretaria de Infraestrutura e Serviços Públicos",
        ]
    
    for nome in secretarias_padrao:
        Secretaria.objects.get_or_create(secretaria=nome)

@receiver(post_migrate)
def importar_veiculos(sender, **kwargs):
    """
    Lê um arquivo XLSX e cadastra veículos que ainda não existem no banco.
    O arquivo deve estar em settings.BASE_DIR / 'dados/veiculos.xlsx'
    """
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'dados', 'veiculos.xlsx')

    if not os.path.exists(caminho_arquivo):
        print(f"[IMPORTAR VEICULOS] Arquivo não encontrado: {caminho_arquivo}")
        return

    try:
        df = pd.read_excel(caminho_arquivo, dtype={
            'cod_veiculo': int,
            'veiculo': str,
            'placa': str,
            'tipocombustível': int
        })

        for _, row in df.iterrows():
            cod = row['cod_veiculo']
            desc = row['veiculo']
            placa = row.get('placa') if pd.notna(row.get('placa')) else None
            combustivel = int(row['tipocombustível'])

            if not Veiculo.objects.filter(cod_veiculo=cod).exists():
                Veiculo.objects.create(
                    cod_veiculo=cod,
                    descricao=desc,
                    placa=placa,
                    combustivel=combustivel,
                    cota=Cota.objects.get(pk=1),  # Ajustar se necessário
                    cota_qnt=1
                )
                print(f"[IMPORTAR VEICULOS] Veículo {cod} - {desc} cadastrado.")

    except Exception as e:
        print(f"[IMPORTAR VEICULOS] Erro ao importar: {e} {desc}")

