from django.urls import path
from .controle import controle

urlpatterns = [
    path('relatorio/', AddedAbastecimento.as_view(), name='abastecimento-added'),
]
