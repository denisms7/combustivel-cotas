from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class Cota(models.Model):
    TIPO_CHOICES = [
        (1, _('Semanal')),
        (2, _('Mensal')),
        ]
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    cadastrado_por = models.ForeignKey(User, default=1, on_delete=models.PROTECT, verbose_name=_('Cadastrado por'), null=True, blank=True)
    nome = models.CharField(max_length=150, verbose_name=_('Nome'))
    litros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Litros'))
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_CHOICES, verbose_name='Tipo')

    def __str__(self):
        return f'{self.nome} L{self.litros} - {self.tipo}'



class Veiculo(models.Model):
    COMBUSTIVEL_CHOICES = [
        (1, _('Gasolina')),
        (2, _('Diesel S10')),
        (3, _('Alcool')),
        ]
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    cadastrado_por = models.ForeignKey(User, default=1, on_delete=models.PROTECT, verbose_name=_('Cadastrado por'))
    descricao = models.CharField(max_length=150, verbose_name=_('Descrição'))
    placa = models.CharField(max_length=150, verbose_name=_('Placa'))
    combustivel = models.PositiveSmallIntegerField(default=1, choices=COMBUSTIVEL_CHOICES, verbose_name='Tipo')
    cota = models.ForeignKey(Cota, verbose_name=_('Cota'), default=1, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.placa} {self.descricao} - {self.combustivel}'