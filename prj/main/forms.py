from django import forms
from dal import autocomplete
from .models import Mesto, Cast, Obrazek

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
            forward=['mesto']
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
        widget=forms.HiddenInput()
    )

    max_cena = forms.DecimalField(
        required=False,
        widget=forms.HiddenInput()
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
