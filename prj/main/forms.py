from django import forms
from dal import autocomplete
from .models import Nemovitost, Lokalita


class FiltrForm(forms.Form):
    TYPY = [
        ('', '------'),
        ('byt', 'Byt'),
        ('dum', 'Dům'),
        ('pozemek', 'Pozemek'),
    ]

    STAVY = [
        ('', '------'),
        ('novostavba', 'Novostavba'),
        ('k_rekonstrukci', 'K rekonstrukci'),
        ('dobry', 'Dobrý stav'),
    ]

    # Autocomplete podle města
    mesto = forms.ModelChoiceField(
        queryset=Lokalita.objects.all().order_by('mesto').distinct('mesto'),
        required=False,
        label='Město',
        widget=autocomplete.ModelSelect2(
            url='mesto-autocomplete',
        )
    )

    # Autocomplete podle části – závislá na městě
    cast = forms.ModelChoiceField(
        queryset=Lokalita.objects.all().order_by('cast'),
        required=False,
        label='Městská část',
        widget=autocomplete.ModelSelect2(
            url='cast-autocomplete',
            forward=['mesto'],  # závislost na poli 'mesto'
        )
    )

    min_cena = forms.DecimalField(
        label='Minimální cena',
        required=False,
        decimal_places=2,
        max_digits=10,
    )

    max_cena = forms.DecimalField(
        label='Maximální cena',
        required=False,
        decimal_places=2,
        max_digits=10,
    )

    typ = forms.ChoiceField(
        label='Typ nemovitosti',
        choices=TYPY,
        required=False,
    )

    stav = forms.ChoiceField(
        label='Stav',
        choices=STAVY,
        required=False,
    )

    lokalita = forms.ModelChoiceField(
        queryset=Lokalita.objects.all(),
        required=False,
        label='Lokalita',
    )

    # volitelný výchozí typ přes GET
    def __init__(self, *args, **kwargs):
        typ_default = kwargs.pop('typ_default', None)
        super().__init__(*args, **kwargs)

        if typ_default:
            self.fields['typ'].initial = typ_default
