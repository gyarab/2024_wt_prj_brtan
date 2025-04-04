"""
URL configuration for prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views  # Import funkcí z views.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Cesta pro domovskou stránku
    path('detail/<int:id>/', views.detail, name='detail'),  # Cesta pro detail nemovitosti
    path('filtrovani/', views.filtrovani_view, name='filtrovani'),  # Cesta pro filtrované nemovitosti
    path('nabidky/', views.nabidky_view, name='nabidky'),  # Cesta pro zobrazení nabídek
    path('admin/', admin.site.urls),  # Cesta pro admin rozhraní
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
