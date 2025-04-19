from django.shortcuts import render
from .models import Nemovitost  # Přidání modelu Mesto a Cast
from .forms import FiltrForm
from dal import autocomplete
from .models import Lokalita

def home(request):
    return render(request, 'main/home.html')

def detail(request, id):
    try:
        nemovitost = Nemovitost.objects.get(id=id)
    except Nemovitost.DoesNotExist:
        nemovitost = None
    return render(request, 'main/detail.html', {'nemovitost': nemovitost})

def filtrovani_view(request):
    form = FiltrForm(request.GET or None)

    nemovitosti = Nemovitost.objects.all()

    if form.is_valid():
        mesto = form.cleaned_data.get('mesto')
        cast = form.cleaned_data.get('cast')
        typ = form.cleaned_data.get('typ')
        stav = form.cleaned_data.get('stav')
        min_cena = form.cleaned_data.get('min_cena')
        max_cena = form.cleaned_data.get('max_cena')

        if mesto:
            nemovitosti = nemovitosti.filter(lokalita__mesto=mesto)
        if cast:
            nemovitosti = nemovitosti.filter(lokalita__cast=cast)
        if typ:
            nemovitosti = nemovitosti.filter(typ=typ)
        if stav:
            nemovitosti = nemovitosti.filter(stav=stav)
        if min_cena:
            nemovitosti = nemovitosti.filter(cena__gte=min_cena)
        if max_cena:
            nemovitosti = nemovitosti.filter(cena__lte=max_cena)

    return render(request, 'main/filtrovani.html', {
        'form': form,
        'nemovitosti': nemovitosti if request.GET else None,
    })

def nabidky_view(request):
    nemovitosti = Nemovitost.objects.all()
    return render(request, 'main/nabidky.html', {'nemovitosti': nemovitosti})

# autocomplete.py nebo views.py
class MestoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Lokalita.objects.all()

        # Pokud je vyhledávací dotaz, omezíme podle něj výsledky
        if self.q:
            qs = qs.filter(mesto__icontains=self.q)

        # Zajištění, že se města nezobrazují vícekrát (jedno město pouze jednou)
        qs = qs.distinct('mesto')  # Přidání distinct pro jedinečná města
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
