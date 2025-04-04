from django import forms
from .models import Nemovitost
from .models import Lokalita
class FiltrForm(forms.Form):
    min_cena = forms.DecimalField(required=False, label="Minimální cena", max_digits=10, decimal_places=2)
    max_cena = forms.DecimalField(required=False, label="Maximální cena", max_digits=10, decimal_places=2)
    typ = forms.ChoiceField(choices=[('byt', 'Byt'), ('dum', 'Dům'), ('pozemek', 'Pozemek')], required=False, label="Typ nemovitosti")
    lokalita = forms.ModelChoiceField(queryset=Lokalita.objects.all(), required=False, label="Lokalita")
    stav = forms.ChoiceField(choices=[('novostavba', 'Novostavba'), ('k_rekonstrukci', 'K rekonstrukci'), ('dobry', 'Dobrý stav')], required=False, label="Stav nemovitosti")
