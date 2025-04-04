from django.shortcuts import render
from .models import Nemovitost  # Předpokládám, že máte model Nemovitost

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
def filtrovani(request):
    nemovitosti = Nemovitost.objects.all()  # Sem přidejte filtrování dle požadavků
    return render(request, 'main/filtrovani.html', {'nemovitosti': nemovitosti})  # Předání seznamu do šablony

# Funkce pro zobrazení nabídek nemovitostí
def nabidky(request):
    nemovitosti = Nemovitost.objects.all()
    return render(request, 'main/nabidky.html', {'nemovitosti': nemovitosti})

