from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError

class Marca(models.Model):
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    marca = models.CharField(max_length=70, verbose_name=_('Marca'), unique=True)
    def __str__(self):
        return f'{self.marca}'

class TipoCombustivel(models.Model):
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    combustivel = models.CharField(max_length=70, verbose_name=_('Combustivel'), unique=True)
    def __str__(self):
        return f'{self.combustivel}'

class TipoPropriedade(models.Model):
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    propriedade = models.CharField(max_length=50, verbose_name="Propriedade")
    def __str__(self):
        return f"{self.propriedade}"


class Veiculo(models.Model):

    cod_veiculo = models.PositiveIntegerField(verbose_name=_('ID Veículo'), unique=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    alterado_em = models.DateTimeField(auto_now=True, verbose_name=_('Data de Alteração'))
    ativo = models.BooleanField(default=True, verbose_name=_('Ativo'))
    descricao = models.CharField(max_length=150, verbose_name=_('Descrição'))

    tipo_propriedade = models.ForeignKey(
        TipoPropriedade,
        on_delete=models.PROTECT,
        verbose_name="Tipo de Propriedade"
    )

    placa = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[
            RegexValidator(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', _('Formato de placa inválido'))
        ],
        verbose_name=_('Placa')
    )
    renavam = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\d{9,11}$', _('RENAVAM inválido'))],
        verbose_name=_('RENAVAM')
    )

    tipocombustivel = models.ForeignKey(TipoCombustivel, verbose_name='Combustivel', on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, verbose_name=_('Marca'), on_delete=models.PROTECT)
    ano_fabricacao = models.IntegerField(verbose_name=_('Ano de Fabricação'), validators=[
        MinValueValidator(1900, _('Ano de fabricação deve ser maior que 1900')),
        MaxValueValidator(2100, _('Ano de fabricação deve ser menor que 2100')),
    ], null=True, blank=True)
    ano_modelo = models.IntegerField(verbose_name=_('Ano do Modelo'), validators=[
        MinValueValidator(1900, _('Ano do modelo deve ser maior que 1900')),
        MaxValueValidator(2100, _('Ano do modelo deve ser menor que 2100')),
    ], null=True, blank=True)

    class Meta:
        verbose_name = _('Veículo')
        verbose_name_plural = _('Veículos')
        ordering = ['marca__marca', 'descricao']

    def clean(self):
        # Verifica placa duplicada
        if self.placa and Veiculo.objects.exclude(pk=self.pk).filter(placa=self.placa).exists():
            raise ValidationError({'placa': _('Já existe um veículo cadastrado com esta placa.')})

        # Verifica renavam duplicado
        if self.renavam and Veiculo.objects.exclude(pk=self.pk).filter(renavam=self.renavam).exists():
            raise ValidationError({'renavam': _('Já existe um veículo cadastrado com este RENAVAM.')})

    def __str__(self):
        return f'{self.placa or ""} {self.descricao}'
    