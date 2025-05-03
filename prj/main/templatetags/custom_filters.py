from django import template

register = template.Library()

@register.filter
def cz_intcomma(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", "\u00A0")  # nezalomitelná mezera
    except (ValueError, TypeError):
        return value
