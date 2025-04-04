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
    # Inicializujeme formulář
    form = FiltrForm(request.GET)

    # Načteme všechny nemovitosti
    nemovitosti = Nemovitost.objects.all()

    # Pokud byl formulář odeslán a je validní, filtrujeme podle hodnot
    if form.is_valid():
        min_cena = form.cleaned_data.get('min_cena')
        max_cena = form.cleaned_data.get('max_cena')
        typ = form.cleaned_data.get('typ')
        lokalita = form.cleaned_data.get('lokalita')
        stav = form.cleaned_data.get('stav')

        if min_cena:
            nemovitosti = nemovitosti.filter(cena__gte=min_cena)
        if max_cena:
            nemovitosti = nemovitosti.filter(cena__lte=max_cena)
        if typ:
            nemovitosti = nemovitosti.filter(typ=typ)
        if lokalita:
            nemovitosti = nemovitosti.filter(lokalita=lokalita)
        if stav:
            nemovitosti = nemovitosti.filter(stav=stav)

    return render(request, 'main/filtrovani.html', {'form': form, 'nemovitosti': nemovitosti})


# Funkce pro zobrazení nabídek nemovitostí

def nabidky_view(request):
    nemovitosti = Nemovitost.objects.all()
    return render(request, 'main/nabidky.html', {'nemovitosti': nemovitosti})
  # Předání seznamu nabídek do šablony

