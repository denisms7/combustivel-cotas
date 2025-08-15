from django.urls import path
from .views import BuscaAbastecimento, AddedAbastecimento, BuscaVeiculos

urlpatterns = [
    path('', BuscaAbastecimento.as_view(), name='inicio'),
    path('added/', AddedAbastecimento.as_view(), name='abastecimento-added'),
    path('carros/', BuscaVeiculos.as_view(), name='BuscaVeiculos'),
]
