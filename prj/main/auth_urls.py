from django.urls import path, include
from . import auth_views

urlpatterns = [
    # Custom auth views
    path('login/', auth_views.login_view, name='custom_login' ),
    path('logout/', auth_views.logout_view, name='custom_logout'),
    
    # Include all allauth URLs for backend processing
    path('', include('allauth.urls')),
]
