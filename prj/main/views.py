from django.shortcuts import render
from .models import Nemovitost  # Předpokládám, že máte model Nemovitost
from .forms import FiltrForm

# Funkce pro zobrazení domovské stránky
def home(request):
    return render(request, 'main/home.html')  # Cesta k šabloně 'home.html' ve složce 'main'

# Funkce pro zobrazení detailu nemovitosti
def detail(request, id):
    try:
        nemovitost = Nemovitost.objects.get(id=id)  # Získání konkrétní nemovitosti podle ID
    except Nemovitost.DoesNotExist:
        nemovitost = None  # Pokud nemovitost neexistuje, nastavíme na None
    return render(request, 'main/detail.html', {'nemovitost': nemovitost})  # Předání objektu do šablony

# Funkce pro zobrazení filtrovaných nemovitostí




def filtrovani_view(request):
    # Defaultní hodnota pro filtr 'typ' z URL parametrů
    typ_default = request.GET.get('typ', None)
    
    # Vytvoření formuláře s aktuálními GET daty, pokud jsou
    form = FiltrForm(request.GET or None)

    # Počáteční dotaz na všechna nemovitost
    nemovitosti = Nemovitost.objects.all()

    # Filtrace podle GET parametrů
    if form.is_valid():
        mesto = form.cleaned_data.get('mesto')
        cast = form.cleaned_data.get('cast')

        # Filtrace podle města
        if mesto:
            nemovitosti = nemovitosti.filter(lokalita__mesto=mesto)

        # Filtrace podle městské části
        if cast:
            nemovitosti = nemovitosti.filter(lokalita__cast=cast)
    
        # Další filtrace podle POST dat (pokud je požadováno)
        if request.method == 'POST':
            form = FiltrForm(request.POST)
            if form.is_valid():
                # Filtrace podle ceny
                if form.cleaned_data['min_cena']:
                    nemovitosti = nemovitosti.filter(cena__gte=form.cleaned_data['min_cena'])

                if form.cleaned_data['max_cena']:
                    nemovitosti = nemovitosti.filter(cena__lte=form.cleaned_data['max_cena'])

                # Filtrace podle typu nemovitosti
                if form.cleaned_data['typ']:
                    nemovitosti = nemovitosti.filter(typ=form.cleaned_data['typ'])

                # Filtrace podle lokality
                if form.cleaned_data['lokalita']:
                    nemovitosti = nemovitosti.filter(lokalita=form.cleaned_data['lokalita'])

                # Filtrace podle stavu
                if form.cleaned_data['stav']:
                    nemovitosti = nemovitosti.filter(stav=form.cleaned_data['stav'])
            else:
                nemovitosti = None  # Pokud formulář není platný

    # Vykreslení stránky s formulářem a výsledky
    return render(request, 'main/filtrovani.html', {
        'form': form,
        'nemovitosti': nemovitosti if request.GET else None  # Zobrazení pouze při GET parametrech
    })

# Funkce pro zobrazení nabídek nemovitostí

def nabidky_view(request):
    nemovitosti = Nemovitost.objects.all()
    return render(request, 'main/nabidky.html', {'nemovitosti': nemovitosti})
  # Předání seznamu nabídek do šablony

