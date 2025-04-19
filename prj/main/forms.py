from django import forms
from dal import autocomplete
from .models import Lokalita

TYPY_NEMOVITOSTI = [
    ('byt', 'Byt'),
    ('dum', 'Dům'),
    ('pozemek', 'Pozemek'),
]

STAVY_NEMOVITOSTI = [
    ('novostavba', 'Novostavba'),
    ('k_rekonstrukci', 'K rekonstrukci'),
    ('dobry', 'Dobrý stav'),
]

class FiltrForm(forms.Form):
    # Získání unikátních měst
    mesto_choices = set(Lokalita.objects.values_list('mesto', flat=True))
    
    # Získání unikátních městských částí, ale odstraníme hodnoty None
    cast_choices = set(Lokalita.objects.values_list('cast', flat=True))
    cast_choices = [cast for cast in cast_choices if cast is not None]  # Filtrujeme None hodnoty

    # Město bude výběr s unikátními hodnotami
    mesto = forms.ChoiceField(
        choices=[('', 'Vyberte město')] + [(mesto, mesto) for mesto in sorted(mesto_choices)],
        required=False,
        label='Město',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # Městská část bude výběr s unikátními hodnotami
    cast = forms.ChoiceField(
        choices=[('', 'Vyberte část')] + [(cast, cast) for cast in sorted(cast_choices)],
        required=False,
        label='Městská část',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    typ = forms.ChoiceField(
        choices=[('', '---------')] + TYPY_NEMOVITOSTI,
        required=False,
        label='Typ nemovitosti'
    )

    stav = forms.ChoiceField(
        choices=[('', '---------')] + STAVY_NEMOVITOSTI,
        required=False,
        label='Stav'
    )

    min_cena = forms.DecimalField(
        required=False,
        label='Minimální cena',
        widget=forms.NumberInput(attrs={'placeholder': 'např. 1000000'})
    )

    max_cena = forms.DecimalField(
        required=False,
        label='Maximální cena',
        widget=forms.NumberInput(attrs={'placeholder': 'např. 5000000'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'data' in kwargs:
            data = kwargs['data']
            if 'mesto' in data:
                self.fields['mesto'].initial = data.get('mesto')
            if 'cast' in data:
                self.fields['cast'].initial = data.get('cast')

            # Získání unikátních měst
        mesto_choices = set(Lokalita.objects.values_list('mesto', flat=True))
            # Získání unikátních městských částí, ale odstraníme hodnoty None
        cast_choices = set(Lokalita.objects.values_list('cast', flat=True))
        cast_choices = [cast for cast in cast_choices if cast is not None]  # Filtrujeme None hodnoty
