"""
Define the views used to render the AMP application.
"""

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

"""
                             AUTHENTICATION
"""
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
            return redirect(dashboard)
        else:
            return render(request, 'login.html', {"error": True})
    else:
        return render(request, 'login.html')

def auth_logout(request):
    """
    Logout the currently logged in user.
    """
    logout(request)
    return redirect(home)

"""
                             GENERAL
"""
def home(request):
    """
    Home page for the AMP application.
    """
    return render(request, 'home.html')

"""
                             APP
"""
def dashboard(request):
    """
    Main dashboard for AMP application.
    """
    return render(request, 'dashboard.html')
