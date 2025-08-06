from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Cota

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
