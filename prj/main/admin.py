from django.contrib import admin
from .models import Klient, MajitelNemovitosti, Nemovitost, Transakce, Obrazek, Mesto, Cast
from django.utils.html import format_html


# Registrace administrátorské třídy pro model Klient
class KlientAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'email', 'telefon')  # Co se zobrazí v seznamu klientů
    search_fields = ('jmeno', 'email', 'telefon')  # Možnost hledání
    list_filter = ('email',)  # Filtrování podle emailu

# Registrace administrátorské třídy pro model MajitelNemovitosti
class MajitelNemovitostiAdmin(admin.ModelAdmin):
    list_display = ('klient', 'poznamky')  # Zobrazení klienta a poznámky
    search_fields = ('klient__jmeno',)  # Možnost hledání podle jména klienta


class MestoAdmin(admin.ModelAdmin):
    search_fields = ['nazev']  


class CastAdmin(admin.ModelAdmin):
    search_fields = ['nazev']  


class ObrazekInline(admin.TabularInline):  # Pro více obrázků v adminu
    model = Obrazek
    extra = 1  # Počet prázdných formulářů pro nový obrázek

# Registrace administrátorské třídy pro model Nemovitost
class NemovitostAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'cena', 'majitel', 'rozloha', 'typ', 'stav', 'obrazek_preview')
    search_fields = ('nazev', 'popis')
    list_filter = ('cena', 'majitel', 'typ', 'stav')
    inlines = [ObrazekInline]  # Možnost přidat více obrázků v adminu
    autocomplete_fields = ['mesto', 'cast']  # Autocomplete pro město a část
    def obrazek_preview(self, obj):
        if obj.obrazek:
            return format_html('<img src="{}" width="150" />', obj.obrazek.url)
        return "Žádný obrázek"

    obrazek_preview.short_description = "Náhled obrázku"

class ObrazekAdmin(admin.ModelAdmin):
    list_display = ('nemovitost', 'obrazek', 'popis')  # Zobrazení obrázků
    search_fields = ('popis',)

# Registrace administrátorské třídy pro model Transakce
class TransakceAdmin(admin.ModelAdmin):
    list_display = ('klient', 'nemovitost', 'datum_transakce', 'cena', 'typ_transakce')  # Zobrazení transakcí
    search_fields = ('klient__jmeno', 'nemovitost__nazev')  # Možnost hledání podle jména klienta a názvu nemovitosti
    list_filter = ('typ_transakce', 'datum_transakce')  # Filtrování podle typu transakce a data

# Registrace všech modelů
admin.site.register(Klient, KlientAdmin)
admin.site.register(MajitelNemovitosti, MajitelNemovitostiAdmin)
admin.site.register(Nemovitost, NemovitostAdmin)
admin.site.register(Transakce, TransakceAdmin)
admin.site.register(Obrazek, ObrazekAdmin)
admin.site.register(Mesto, MestoAdmin)  
admin.site.register(Cast, CastAdmin)    

admin.site.site_header = "Správa nemovitostí"