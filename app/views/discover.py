"""
Define the views used to render the AMP Discover pages.
"""

from django.shortcuts import render, redirect

def home(request):
    """
    Home page for the AMP application.
    """
    if request.user.is_authenticated():
        return redirect('dashboard-home')

    return render(request, 'discover/home.html')
