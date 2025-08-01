from django.urls import path
from .views import BuscaAbastecimento, AddedAbastecimento

urlpatterns = [
    path('', BuscaAbastecimento.as_view(), name='inicio'),
    path('/added/', AddedAbastecimento.as_view(), name='abastecimento-added'),
]
