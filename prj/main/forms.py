from django import forms
from dal import autocomplete
from .models import Mesto, Cast

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
    mesto_choices = set(Mesto.objects.values_list('nazev', flat=True))
    cast_choices = set(Cast.objects.values_list('nazev', flat=True))

    
    # Získání unikátních městských částí, ale odstraníme hodnoty None
    cast_choices = [cast for cast in cast_choices if cast is not None]  # Filtrujeme None hodnoty

    # Město bude výběr s unikátními hodnotami
    mesto = forms.ModelChoiceField(
        queryset=Mesto.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='autocomplete-mesto'),
        label='Město'
    )
    cast = forms.ModelChoiceField(
        queryset=Cast.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='autocomplete-cast',
            forward=['mesto'],  # tady je propojení
        ),
        label='Městská část'
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
    
    def clean(self):
        cleaned_data = super().clean()
        min_cena = cleaned_data.get('min_cena')
        max_cena = cleaned_data.get('max_cena')

        if min_cena and min_cena < 0:
            self.add_error('min_cena', 'Cena nemůže být záporná.')

        if max_cena and max_cena < 0:
            self.add_error('max_cena', 'Cena nemůže být záporná.')

        if min_cena and max_cena and min_cena > max_cena:
            raise forms.ValidationError("Minimální cena nemůže být vyšší než maximální.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'data' in kwargs:
            data = kwargs['data']
            if 'mesto' in data:
                self.fields['mesto'].initial = data.get('mesto')
            if 'cast' in data:
                self.fields['cast'].initial = data.get('cast')

            # Získání unikátních měst
        mesto_choices = set(Mesto.objects.values_list('nazev', flat=True))
        cast_choices = set(Cast.objects.values_list('nazev', flat=True))
        cast_choices = [cast for cast in cast_choices if cast is not None]  # Filtrujeme None hodnoty

