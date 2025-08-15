from django.contrib import admin
from .models import Cota, Veiculo, Abastecimento
from import_export import resources, fields
from import_export.admin import ExportMixin


# Resource do Abastecimento
class AbastecimentoResource(resources.ModelResource):

    class Meta:
        model = Abastecimento
        fields = (
            'cadastrado_em', 
            'cadastrado_por__username', 
            'veiculo__descricao', 
            'veiculo__placa',
            'combustivel', 
            'veiculo__cota__litros', 
            'justificativa'
                )  # campos que deseja exportar
        export_order = (
            'cadastrado_em', 
            'cadastrado_por__username', 
            'veiculo__descricao', 
            'veiculo__placa',
            'combustivel', 
            'veiculo__cota__litros', 
            'justificativa'
            )





@admin.register(Cota)
class CotaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'litros','tipo'] # ver tabela
    search_fields = ['nome','tipo']
    readonly_fields = ['cadastrado_em'] # campos somente leitura
    list_per_page = 25  # quantidade de registros por página
    ordering = ['-cadastrado_em']  # do mais recente para o mais antigo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    readonly_fields = ['cadastrado_em'] # campos somente leitura
    list_display = ['cod_veiculo', 'descricao','placa'] # ver tabela
    search_fields = ['descricao', 'placa']  # pesquisa
    list_filter = ['combustivel', 'cota']   # filtros
    list_per_page = 25  # quantidade de registros por página
    ordering = ['-cadastrado_em']  # do mais recente para o mais antigo

@admin.register(Abastecimento)
class AbastecimentoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['cadastrado_em','cadastrado_por','veiculo'] # ver tabela
    search_fields = ['veiculo__descricao','veiculo__placa']  # pesquisa pela descrição e placa do veículo
    list_filter = ['veiculo__combustivel']  # filtros
    readonly_fields = ['cadastrado_em','cadastrado_por','alterado_em'] # campos somente leitura
    list_per_page = 25  # quantidade de registros por página
    ordering = ['-cadastrado_em']  # do mais recente para o mais antigo

    resource_class = AbastecimentoResource