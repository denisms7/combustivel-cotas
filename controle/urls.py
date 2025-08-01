from django.urls import path
from .views import BuscaAbastecimento

urlpatterns = [
    path('', BuscaAbastecimento.as_view(), name='abastecimento-busca'),
]
