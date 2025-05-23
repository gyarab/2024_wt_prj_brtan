from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Nemovitost, Mesto, Cast, OblibenaNemovitost
from .forms import FiltrForm

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_like(request, nemovitost_id):
    nemovitost = get_object_or_404(Nemovitost, pk=nemovitost_id)
    user = request.user

    oblibena = OblibenaNemovitost.objects.filter(uzivatel=user, nemovitost=nemovitost).first()

    if oblibena:
        oblibena.delete()
        liked = False
    else:
        OblibenaNemovitost.objects.create(user=user, nemovitost=nemovitost)
        liked = True

    total_likes = OblibenaNemovitost.objects.filter(nemovitost=nemovitost).count()

    return JsonResponse({
        'liked': liked,
        'total_likes': total_likes,
        'error': None,
    })

@login_required
def oblibene_nemovitosti_view(request):
    uzivatel = request.user
    oblibene = OblibenaNemovitost.objects.filter(uzivatel=uzivatel)
    nemovitosti = [o.nemovitost for o in oblibene]

    return render(request, 'main/oblibene_nemovitosti.html', {'nemovitosti': nemovitosti})

def home(request):
    nove_nabidky = Nemovitost.objects.order_by('-id')[:5]
    return render(request, 'main/home.html', {'nove_nabidky': nove_nabidky})

def detail(request, id):
    nemovitost = get_object_or_404(Nemovitost, id=id)
    return render(request, 'main/detail.html', {'nemovitost': nemovitost})

def filtrovani_view(request):
    user = request.user
    form = FiltrForm(request.GET or None)
    form.fields['cast'].queryset = Cast.objects.select_related('mesto').all()

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
        if min_cena is not None:
            nemovitosti = nemovitosti.filter(cena__gte=min_cena)
        if max_cena is not None:
            nemovitosti = nemovitosti.filter(cena__lte=max_cena)

    if user.is_authenticated:
        liked_ids = set(
            OblibenaNemovitost.objects.filter(uzivatel=user, nemovitost__in=nemovitosti)
            .values_list('nemovitost_id', flat=True)
        )
    else:
        liked_ids = set()

    nemovitosti = nemovitosti.order_by('-id')  # nebo jiné řazení

    # přidej is_liked atribut k nemovitostem
    for nemovitost in nemovitosti:
        nemovitost.is_liked = nemovitost.id in liked_ids

    paginator = Paginator(nemovitosti, 9)  # 9 výsledků na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # předat oblíbené nemovitosti id, pokud chceš použít i jinde v šabloně
    oblibene_ids = liked_ids if user.is_authenticated else set()

    return render(request, 'main/filtrovani.html', {
        'form': form,
        'nemovitosti': page_obj,
        'oblibene': oblibene_ids,
    })

def nabidky_view(request):
    nemovitosti = Nemovitost.objects.all()
    return render(request, 'main/nabidky.html', {'nemovitosti': nemovitosti})
