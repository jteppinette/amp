"""
Define the views used to render the AMP application.
"""

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.views.generic.edit import CreateView

from django.core.urlresolvers import reverse_lazy

# Company Model
from api.models import Company

# Notification Model
from api.models import Notification

# Accessor Models
from api.models import Employee, Contractor

# Permission Models
from api.models import Permission, Log

# Request Models
from api.models import EmployeeRequest, ContractorRequest

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

"""
                             REQUESTS
"""
def request_success(request):
    """
    Render the request success page.
    """
    return render(request, 'request_success.html')


class NewEmployeeRequest(CreateView):
    """
    Create a new employee request.
    """
    template_name = 'new_employee_request.html'
    model = EmployeeRequest
    success_url = reverse_lazy(request_success)

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save()

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return redirect(self.success_url)


class NewContractorRequest(CreateView):
    """
    Create a new contractor request.
    """
    template_name = 'new_contractor_request.html'
    model = ContractorRequest
    success_url = reverse_lazy(request_success)

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save()

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return redirect(self.success_url)
