"""
Define the views used to render the AMP Authentication pages.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render, redirect

def auth_login(request):
    """
    Login in a user based on the provided email and password.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)

            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
        else:
            messages.add_message(request, messages.ERROR, 'Your username and password did not match. Please try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def auth_logout(request):
    """
    Logout the currently logged in user.
    """
    logout(request)
    return redirect('home')


