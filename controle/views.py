from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Abastecimento
from .forms import AbastecimentoForm
from datetime import datetime

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
        form.instance.cadastrado_por = self.request.user
        messages.success(self.request, "Registro salvo com sucesso.")
        return super().form_valid(form)
