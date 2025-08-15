from django.contrib import admin
from .models import Cota, Veiculo, Abastecimento

@admin.register(Cota)
class CotaAdmin(admin.ModelAdmin):
    search_fields = ['nome']

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    search_fields = ['descricao', 'placa']  # pesquisa
    list_filter = ['combustivel', 'cota']   # filtros


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    search_fields = [
        'veiculo__descricao',
        'veiculo__placa'
    ]  # pesquisa pela descrição e placa do veículo
    list_filter = [
        'veiculo__combustivel'
    ]  # filt