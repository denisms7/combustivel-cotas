from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Abastecimento, Cota, Veiculo
from .forms import AbastecimentoForm
from datetime import datetime
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear
from django.utils.timezone import localtime

class BuscaAbastecimento(LoginRequiredMixin, ListView):
    model = Abastecimento
    template_name = 'controle/busca.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            try:
                data_formatada = datetime.strptime(query, "%Y-%m-%d").date()
                queryset = queryset.filter(
                    Q(veiculo__icontains=query) | Q(cadastrado_em=data_formatada)
                )
            except ValueError:
                queryset = queryset.filter(
                    Q(veiculo__descricao__icontains=query) | Q(veiculo__placa__icontains=query)
                )

        return queryset.order_by('-cadastrado_em')


class AddedAbastecimento(LoginRequiredMixin, CreateView):
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'controle/cadastro.html'
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        veiculo = form.cleaned_data['veiculo']
        data_atual = localtime().date()
        cota_tipo = veiculo.cota.tipo  # 1 = semanal, 2 = mensal

        abastecimentos = Abastecimento.objects.filter(veiculo=veiculo)

        if cota_tipo == 1:  # Semanal
            semana_atual = data_atual.isocalendar().week
            ano_atual = data_atual.isocalendar().year

            # Contar abastecimentos da semana atual
            existe = abastecimentos.annotate(
                semana=ExtractWeek('cadastrado_em'),
                ano=ExtractYear('cadastrado_em')
            ).filter(
                semana=semana_atual,
                ano=ano_atual
            ).count()
            

            # Aqui você deve acessar a cota correta
            cota_qnt = veiculo.cota_qnt  # supondo que o campo cota_qnt esteja no modelo Veiculo

                    
            if existe >= cota_qnt:
                messages.warning(self.request, f'Já existe um abastecimento para o veículo: {veiculo.descricao}. Total de abastecimentos {existe}')
                return self.form_invalid(form)

        elif cota_tipo == 2:  # Mensal
            mes_atual = data_atual.month
            ano_atual = data_atual.year

            existe = abastecimentos.annotate(
                mes=ExtractMonth('cadastrado_em'),
                ano=ExtractYear('cadastrado_em')
            ).filter(
                mes=mes_atual,
                ano=ano_atual
            ).exists()

            if existe:
                messages.warning(self.request, f'Já existe um abastecimento para o veículo {veiculo} neste mês.')
                return self.form_invalid(form)

        # Salva normalmente se não houver conflito
        form.instance.cadastrado_por = self.request.user
        messages.success(self.request, "Registro salvo com sucesso.")
        return super().form_valid(form)
    


class BuscaVeiculos(LoginRequiredMixin, ListView):
    model = Veiculo
    template_name = 'controle/veiculos.html'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(descricao__icontains=query) | Q(placa__icontains=query) | Q(cod_veiculo__icontains=query)
            )

        return queryset.order_by('-cadastrado_em') 