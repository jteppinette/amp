from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.conf import settings

from django.shortcuts import render, redirect

def auth_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)

            next_page = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
            return redirect(next_page)
        else:
            messages.add_message(request, messages.ERROR, 'Your username and password did not match. Please try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def auth_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
