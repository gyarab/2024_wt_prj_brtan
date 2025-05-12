from django.contrib import admin
from .models import Klient, MajitelNemovitosti, Nemovitost, Transakce, Obrazek, Mesto, Cast
from django.utils.html import format_html
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets

class KlientAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'email', 'telefon')
    search_fields = ('jmeno', 'email', 'telefon')
    list_filter = ('email',)

class MajitelNemovitostiAdmin(admin.ModelAdmin):
    list_display = ('klient', 'poznamky')
    search_fields = ('klient__jmeno',)

class MestoAdmin(admin.ModelAdmin):
    search_fields = ['nazev']

class CastAdmin(admin.ModelAdmin):
    search_fields = ['nazev']

class ObrazekInline(admin.TabularInline):  # Použijeme TabularInline nebo StackedInline
    model = Obrazek
    extra = 1  # Počet prázdných formulářů pro přidání nových obrázků

class NemovitostAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'cena', 'majitel', 'rozloha', 'typ', 'stav', 'obrazek_preview')
    search_fields = ('nazev', 'popis')
    list_filter = ('cena', 'majitel', 'typ', 'stav')
    inlines = [ObrazekInline]
    autocomplete_fields = ['mesto', 'cast']
    
    def obrazek_preview(self, obj):
        if hasattr(obj, 'obrazek') and obj.obrazek:
            return format_html('<img src="{}" width="150" />', obj.obrazek.url)
        return "Žádný obrázek"
    obrazek_preview.short_description = "Náhled obrázku"

class ObrazekAdmin(admin.ModelAdmin):
    list_display = ['obrazek', 'popis', 'nemovitost']

class TransakceAdmin(admin.ModelAdmin):
    list_display = ('klient', 'nemovitost', 'datum_transakce', 'cena', 'typ_transakce')
    search_fields = ('klient__jmeno', 'nemovitost__nazev')
    list_filter = ('typ_transakce', 'datum_transakce')

admin.site.register(Klient, KlientAdmin)
admin.site.register(MajitelNemovitosti, MajitelNemovitostiAdmin)
admin.site.register(Nemovitost, NemovitostAdmin)
admin.site.register(Transakce, TransakceAdmin)
admin.site.register(Obrazek, ObrazekAdmin)
admin.site.register(Mesto, MestoAdmin)
admin.site.register(Cast, CastAdmin)

admin.site.site_header = "Správa nemovitostí"
