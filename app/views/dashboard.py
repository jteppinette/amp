"""
Define the views used to render the AMP Dashboard pages.
"""

from django.shortcuts import render

def dashboard(request):
    """
    Main dashboard for AMP application.
    """
    return render(request, 'dashboard.html')

