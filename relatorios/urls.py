from django.urls import path
from . import views

urlpatterns = [
    path('relatorio-abastecimento/', views.relatorio_abastecimento, name='rel_abastecimento'),
]
