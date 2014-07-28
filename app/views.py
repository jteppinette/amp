"""
Define the views used to render the AMP application.
"""

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.edit import CreateView, UpdateView

from django.core.urlresolvers import reverse_lazy

# Custom User Model
from django.contrib.auth import get_user_model
from authentication.forms import UserChangeForm

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

            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
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
    if request.user.is_authenticated():
        return redirect('dashboard')

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
                             NEW REQUESTS
"""
class NewEmployeeRequest(SuccessMessageMixin, CreateView):
    """
    Create a new employee request.
    """
    template_name = 'new_employee_request.html'
    model = EmployeeRequest
    success_url = reverse_lazy('home')
    success_message = "Employee request submision was successful! You will be contacted soon."

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save()

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return super(NewEmployeeRequest, self).form_valid(form)


class NewContractorRequest(SuccessMessageMixin, CreateView):
    """
    Create a new contractor request.
    """
    template_name = 'new_contractor_request.html'
    model = ContractorRequest
    success_url = reverse_lazy('home')
    success_message = "Contractor request submision was successful! You will be contacted soon."

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save(commit=True)

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return super(NewContractorRequest, self).form_valid(form)

"""
                             ACCOUNT
"""
class UpdateAccount(SuccessMessageMixin, UpdateView):
    """
    Update the currently logged in users account.
    """
    template_name = 'update_account.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('update_account')
    success_message = "Your account was updated successfully!"

    def get_object(self, queryset=None):
        """
        Get the object that will be updated.
        """
        return self.request.user
