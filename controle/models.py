from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Cota(models.Model):
    TIPO_CHOICES = [
        (1, _('Semanal')),
        (2, _('Mensal')),
        ]
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    nome = models.CharField(max_length=150, verbose_name=_('Nome'))
    litros = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Litros'))
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_CHOICES, verbose_name='Tipo')

    class Meta:
        verbose_name = _('Cota')
        verbose_name_plural = _('Cotas')
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} L{self.litros}'

class Veiculo(models.Model):
    COMBUSTIVEL_CHOICES = [
        (1, _('Gasolina')),
        (2, _('Diesel')),
        (3, _('Flex e Semelhantes')),
        (4, _('Outros')),
        ]
    cod_veiculo = models.IntegerField(verbose_name=_('ID Veículo'), unique=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    descricao = models.CharField(max_length=150, verbose_name=_('Descrição'))
    placa = models.CharField(max_length=150, verbose_name=_('Placa'), null=True, blank=True)
    combustivel = models.PositiveSmallIntegerField(default=1, choices=COMBUSTIVEL_CHOICES, verbose_name='Tipo')
    cota = models.ForeignKey(Cota, verbose_name=_('Cota'), default=1, on_delete=models.PROTECT)
    cota_qnt = models.IntegerField(default=1, verbose_name=_('N Abastecimentos'))

    class Meta:
        verbose_name = _('Veículo')
        verbose_name_plural = _('Veículos')
        ordering = ['descricao']

    def __str__(self):
        return f'{self.placa or ""} {self.descricao}'
    

class Abastecimento(models.Model):
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    cadastrado_por = models.ForeignKey(User, default=1, on_delete=models.PROTECT, verbose_name=_('Cadastrado por'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    veiculo = models.ForeignKey(Veiculo, verbose_name=_('Veiculo'), on_delete=models.PROTECT)
    justificativa = models.TextField(max_length=2000, verbose_name=_('Justificativa'), null=True, blank=True)

    class Meta:
        verbose_name = _('Abastecimento')
        verbose_name_plural = _('Abastecimentos')
        ordering = ['-cadastrado_em']

    def __str__(self):
        return f'{self.veiculo.placa or ""} {self.veiculo.descricao}'