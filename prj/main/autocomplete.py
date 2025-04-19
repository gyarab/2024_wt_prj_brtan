from dal import autocomplete
from .models import Lokalita

class MestoAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        mesta = Lokalita.objects.values_list('mesto', flat=True).distinct()
        if self.q:
            mesta = mesta.filter(mesto__icontains=self.q)
        return list(mesta)

class CastAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        qs = Lokalita.objects.all()
        mesto = self.forwarded.get('mesto')
        if mesto:
            qs = qs.filter(mesto=mesto)
        if self.q:
            qs = qs.filter(cast__icontains=self.q)
        casti = qs.values_list('cast', flat=True).distinct()
        return list(casti)
