from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from main import views
from main.autocomplete import MestoAutocomplete, CastAutocomplete

urlpatterns = [
    # Hlavní stránky
    path('', views.home, name='home'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('filtrovani/', views.filtrovani_view, name='filtrovani'),
    path('nabidky/', views.nabidky_view, name='nabidky'),
    
    # Autocomplete pro formulář
    path('autocomplete/mesto/', MestoAutocomplete.as_view(), name='autocomplete-mesto'),
    path('autocomplete/cast/', CastAutocomplete.as_view(), name='autocomplete-cast'),
    
    # Admin rozhraní
    path('admin/', admin.site.urls),
    
    # Authentication URLs - custom and allauth
    path('accounts/', include('main.auth_urls')),
    
    # Redirect legacy login URLs to our custom login
    path('accounts/login/', RedirectView.as_view(pattern_name='custom_login'), name='account_login'),
    path('accounts/logout/', RedirectView.as_view(pattern_name='custom_logout'), name='account_logout'),
    
    # like/unlike nemovitosti
    path('nemovitost/<int:nemovitost_id>/like/', views.toggle_like, name='toggle_like'),
    path('oblibene_nemovitosti/', views.oblibene_nemovitosti_view, name='oblibene_nemovitosti'),
]

# Nastavení pro nahrané obrázky
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
