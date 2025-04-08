from django import forms
from .models import Nemovitost
from .models import Lokalita

class FiltrForm(forms.Form):
    def __init__(self, *args, **kwargs):
        typ_default = kwargs.pop('typ_default', None)
        super(FiltrForm, self).__init__(*args, **kwargs)
        if typ_default:
            self.fields['typ'].initial = typ_default

    TYPY = [
        ('byt', 'Byt'),
        ('dum', 'Dům'),
        ('pozemek', 'Pozemek'),
    ]

    STAVY = [
        ('', '-------'),  # Prázdná volba
        ('novostavba', 'Novostavba'),
        ('k_rekonstrukci', 'K rekonstrukci'),
        ('dobry', 'Dobrý stav'),
    ]
    mesto = forms.ChoiceField(
        choices=[],
        required=False,
        label="Město"
    )
    cast = forms.ChoiceField(
        choices=[('', '-----')],
        required=False,
        label="Městská část"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Načtení unikátních měst
        mesta = Lokalita.objects.values_list('mesto', flat=True).distinct()
        self.fields['mesto'].choices = [('', '-----')] + [(m, m) for m in mesta]

        # Pokud uživatel zvolil město, načíst odpovídající části
        if 'mesto' in self.data:
            casti = Lokalita.objects.filter(mesto=self.data['mesto']).values_list('cast', flat=True).distinct()
            self.fields['cast'].choices += [(c, c) for c in casti if c]
    


    min_cena = forms.DecimalField(label='Minimální cena', required=False, decimal_places=2, max_digits=10)
    max_cena = forms.DecimalField(label='Maximální cena', required=False, decimal_places=2, max_digits=10)
    typ = forms.ChoiceField(label='Typ nemovitosti', choices=TYPY, required=False)
    lokalita = forms.ModelChoiceField(queryset=Lokalita.objects.all(), label='Lokalita', required=False)
    stav = forms.ChoiceField(label='Stav', choices=STAVY, required=False)
