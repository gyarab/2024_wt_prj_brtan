from django.db import models
from django.core.validators import MinValueValidator



class Klient(models.Model):
    jmeno = models.CharField(max_length=300)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefon = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.jmeno


class MajitelNemovitosti(models.Model):
    klient = models.OneToOneField(Klient, on_delete=models.CASCADE)
    poznamky = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Majitel: {self.klient.jmeno}"


class Lokalita(models.Model):
    mesto = models.CharField(max_length=100, verbose_name='Město')
    cast = models.CharField(max_length=100, verbose_name='Městská část', blank=True, null=True)

    class Meta:
        unique_together = ('mesto', 'cast')
        ordering = ['mesto', 'cast']
        verbose_name = 'Lokalita'
        verbose_name_plural = 'Lokality'

    def __str__(self):
        return f'{self.mesto} – {self.cast}' if self.cast else self.mesto

class Nemovitost(models.Model):
    nazev = models.CharField(max_length=300)
    cena = models.IntegerField(validators=[MinValueValidator(0)])
    popis = models.TextField(blank=True, default="")
    lokalita = models.ForeignKey(Lokalita, on_delete=models.CASCADE, verbose_name="Lokalita")
    majitel = models.ForeignKey(MajitelNemovitosti, on_delete=models.SET_NULL, null=True)

    
    obrazek = models.ImageField(upload_to='nemovitosti/', blank=True, null=True)  # Náhledový obrázek
    dalsi_obrazky = models.ManyToManyField('Obrazek', blank=True, related_name='nemovitosti')   # Vztah pro více obrázků

    rozloha = models.PositiveIntegerField(help_text="Rozloha v m²", null=True, blank=True)
    typ = models.CharField(max_length=100, choices=[
        ('byt', 'Byt'),
        ('dum', 'Dům'),
        ('pozemek', 'Pozemek'),
    ], default='byt')
    stav = models.CharField(max_length=100, choices=[
        ('novostavba', 'Novostavba'),
        ('k_rekonstrukci', 'K rekonstrukci'),
        ('dobry', 'Dobrý stav'),
    ], default='dobry')

    def __str__(self):
        return f"{self.nazev} ({self.cena} Kč)"

class Obrazek(models.Model):
    nemovitost = models.ForeignKey(Nemovitost, related_name='obrazky', on_delete=models.CASCADE)
    obrazek = models.ImageField(upload_to='nemovitosti/')
    popis = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Obrázek pro {self.nemovitost.nazev}"

class Transakce(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    nemovitost = models.ForeignKey(Nemovitost, on_delete=models.CASCADE)
    datum_transakce = models.DateField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    typ_transakce = models.CharField(max_length=50, choices=[('Koupě', 'Koupě'), ('Prodej', 'Prodej')])

    def __str__(self):
        return f"{self.klient.jmeno} - {self.nemovitost.nazev} - {self.typ_transakce} ({self.datum_transakce})"
