from dal import autocomplete
from .models import Mesto, Cast

class MestoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Mesto.objects.all()
        if self.q:
            qs = qs.filter(nazev__icontains=self.q)
        return qs

class CastAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cast.objects.all()
        mesto = self.forwarded.get('mesto', None)
        if mesto:
            qs = qs.filter(mesto_id=mesto)  # filtrujeme podle foreign key
        if self.q:
            qs = qs.filter(nazev__icontains=self.q)
        return qs