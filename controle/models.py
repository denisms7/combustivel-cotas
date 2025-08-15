from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Cota(models.Model):
    TIPO_CHOICES = [
        (1, _('Semanal')),
        (2, _('Mensal')),
        ]
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    nome = models.CharField(max_length=150, verbose_name=_('Nome'))
    litros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Litros'))
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_CHOICES, verbose_name='Tipo')

    def __str__(self):
        return f'{self.nome} L{self.litros}'

class Veiculo(models.Model):
    COMBUSTIVEL_CHOICES = [
        (1, _('Gasolina')),
        (2, _('Diesel S10')),
        (3, _('Flex e Semelhantes')),
        (4, _('Outros')),
        ]
    cod_veiculo = models.IntegerField(verbose_name=_('ID Veículo'), unique=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    descricao = models.CharField(max_length=150, verbose_name=_('Descrição'))
    placa = models.CharField(max_length=150, verbose_name=_('Placa'), null=True, blank=True)
    combustivel = models.PositiveSmallIntegerField(default=1, choices=COMBUSTIVEL_CHOICES, verbose_name='Tipo')
    cota = models.ForeignKey(Cota, verbose_name=_('Cota'), default=1, on_delete=models.PROTECT)
    cota_qnt = models.IntegerField(default=1, verbose_name=_('N Abastecimentos'))

    def __str__(self):
        return f'{self.placa} {self.descricao}'
    

class Abastecimento(models.Model):
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    cadastrado_por = models.ForeignKey(User, default=1, on_delete=models.PROTECT, verbose_name=_('Cadastrado por'))
    veiculo = models.ForeignKey(Veiculo, verbose_name=_('Veiculo'), on_delete=models.PROTECT)
    justificativa = models.TextField(max_length=2000, verbose_name=_('Justificativa'), null=True, blank=True)

    def __str__(self):
        return f'{self.veiculo.placa or ""} {self.veiculo.descricao}'