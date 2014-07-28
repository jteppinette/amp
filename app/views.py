"""
Define the views used to render the AMP application.
"""

from django.shortcuts import render

"""
                             AUTHENTICATION
"""
def login(request):
    """
    Login in a user based on the provided email and password.
    """
    return render(request, 'login.html')

"""
                             GENERAL
"""
def home(request):
    """
    Home page for the AMP application.
    """
    return render(request, 'home.html')

