"""
Define the views used to render the AMP application.
"""

from django.shortcuts import render

def home(request):
    """
    Home page for the AMP application.
    """
    return render(request, 'home.html')

