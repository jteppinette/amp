from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated():
        return redirect('dashboard-home')

    return render(request, 'discover/home.html')
