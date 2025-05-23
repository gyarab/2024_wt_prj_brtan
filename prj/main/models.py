from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Klient(models.Model):
    jmeno = models.CharField(max_length=300)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefon = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.jmeno

    class Meta:
        verbose_name_plural = "Klienti"
        ordering = ['jmeno']  # Seřazení podle jména klienta ve správě admina

class MajitelNemovitosti(models.Model):
    klient = models.OneToOneField(Klient, on_delete=models.CASCADE)
    poznamky = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Majitel: {self.klient.jmeno}"
    class Meta:
        verbose_name_plural = "Majitelé nemovitostí"
    

class Mesto(models.Model):
    nazev = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazev

    class Meta:
        verbose_name_plural = "Města"
        ordering = ['nazev']

class Cast(models.Model):
    nazev = models.CharField(max_length=100)
    mesto = models.ForeignKey(Mesto, on_delete=models.CASCADE, related_name='casti')

    def __str__(self):
        return f"{self.nazev} ({self.mesto.nazev})"
    class Meta:
        verbose_name_plural = "Městské části"
        ordering = ['mesto', 'nazev']


class Nemovitost(models.Model):
    nazev = models.CharField(max_length=300)
    cena = models.IntegerField(validators=[MinValueValidator(0)])
    popis = models.TextField(blank=True, default="")
    majitel = models.ForeignKey(MajitelNemovitosti, on_delete=models.SET_NULL, null=True)
    mesto = models.ForeignKey(Mesto, on_delete=models.SET_NULL, null=True, blank=True)
    cast = models.ForeignKey(Cast, on_delete=models.SET_NULL, null=True, blank=True)
    
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
    class Meta:
        verbose_name_plural = "Nemovitosti"
        ordering = ['-id']  # Seřazení podle ID sestupně ve správě admina
    def pocet_lajku(self):
        return self.lajky.count()
    
class OblibenaNemovitost(models.Model):
    uzivatel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nemovitost = models.ForeignKey('Nemovitost', on_delete=models.CASCADE, related_name='lajky')
    vytvoreno = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uzivatel', 'nemovitost')

class Obrazek(models.Model):
    nemovitost = models.ForeignKey(Nemovitost, related_name='obrazky', on_delete=models.CASCADE)
    obrazek = models.ImageField(upload_to='nemovitosti/')
    popis = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Obrázek pro {self.nemovitost.nazev}"
    class Meta:
        verbose_name_plural = "Obrázky"
        ordering = ['-id']  # Seřazení podle ID sestupně ve správě admina
class Transakce(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    nemovitost = models.ForeignKey(Nemovitost, on_delete=models.CASCADE)
    datum_transakce = models.DateField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    typ_transakce = models.CharField(max_length=50, choices=[('Koupě', 'Koupě'), ('Prodej', 'Prodej')])

    def __str__(self):
        return f"{self.klient.jmeno} - {self.nemovitost.nazev} - {self.typ_transakce} ({self.datum_transakce})"
    class Meta:
        verbose_name_plural = "Transakce"
