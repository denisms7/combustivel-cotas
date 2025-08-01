from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, ProtectedError
from .models import Abastecimento


class BuscaAbastecimento(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Abastecimento
    template_name = 'controle/busca.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(medico__icontains=query) | Q(data__icontains=query)
            )
        return queryset