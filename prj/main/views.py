from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Nemovitost
from .forms import FiltrForm


def home(request):
    nove_nabidky = Nemovitost.objects.order_by('-id')[:3]
    return render(request, 'main/home.html', {'nove_nabidky': nove_nabidky})

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
            nemovitosti = nemovitosti.filter(mesto=mesto)
        if cast:
            nemovitosti = nemovitosti.filter(cast=cast)
        if typ:
            nemovitosti = nemovitosti.filter(typ=typ)
        if stav:
            nemovitosti = nemovitosti.filter(stav=stav)
        if min_cena:
            nemovitosti = nemovitosti.filter(cena__gte=min_cena)
        if max_cena:
            nemovitosti = nemovitosti.filter(cena__lte=max_cena)
    #paginace rozdeleni vysledku do stranek
    paginator = Paginator(nemovitosti, 9)  # 9 výsledků na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    
    return render(request, 'main/filtrovani.html', {
        'form': form,
        'nemovitosti': nemovitosti if request.GET else None,
    })



def nabidky_view(request):
    nemovitosti = Nemovitost.objects.all()
    return render(request, 'main/nabidky.html', {'nemovitosti': nemovitosti})

# autocomplete.py nebo views.py

