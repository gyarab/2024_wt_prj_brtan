from dal import autocomplete
from .models import Lokalita

class MestoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lokalita.objects.order_by('mesto').distinct('mesto')
        if self.q:
            qs = qs.filter(mesto__icontains=self.q)
        return qs

class CastAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lokalita.objects.all()
        mesto = self.forwarded.get('mesto', None)
        if mesto:
            qs = qs.filter(mesto=mesto)
        if self.q:
            qs = qs.filter(cast__icontains=self.q)
        return qs
