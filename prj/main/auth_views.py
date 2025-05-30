from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse

def login_view(request):
    """
    Custom login view that redirects to Google authentication.
    This ensures we only use Google for authentication.
    """
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    # Otherwise show the Google login page
    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    """
    Custom logout confirmation view.
    """
    if request.method == 'POST':
        # Actually log the user out
        logout(request)
        return redirect('home')
    
    # Show the logout confirmation page
    return render(request, 'auth/logout.html')
