"""
Define the views used to render the AMP application.
"""

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView

from django.core.urlresolvers import reverse_lazy

# Custom User Model
from django.contrib.auth import get_user_model
from authentication.forms import UserChangeForm, UserCreationForm

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
            messages.add_message(request, messages.ERROR, 'Your username and password did not match. Please try again.')
            return render(request, 'login.html')
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

"""
                             COMPANY
"""
def company(request):
    """
    Show the four other users in the CIP Manager's company.
    """
    if request.user.title != 'CIP Manager':
        return redirect('dashboard')

    company = request.user.company

    obj_mng = get_user_model().objects
    
    qs = obj_mng.filter(company=company, title='Alternate CIP Manager')
    if qs:
        alternate_cip_manager = qs[0]
    else:
        alternate_cip_manager = None
    qs = obj_mng.filter(company=company, title='Access Control Engineer')
    if qs:
        access_control_engineer = qs[0]
    else:
        access_control_engineer = None
    qs = obj_mng.filter(company=company, title='Training Coordinator')
    if qs:
        training_coordinator = qs[0]
    else:
        training_coordinator = None
    qs = obj_mng.filter(company=company, title='Human Resources')
    if qs:
        human_resources = qs[0]
    else:
        human_resources = None

    return render(request, 'company.html', {
        'alternate_cip_manager': alternate_cip_manager,
        'access_control_engineer': access_control_engineer,
        'training_coordinator': training_coordinator,
        'human_resources': human_resources,
    })

class NewCompanyUser(SuccessMessageMixin, CreateView):
    """
    Create a new contractor request.
    """
    template_name = 'new_company_user.html'
    model = get_user_model()
    form_class = UserCreationForm
    success_url = reverse_lazy('company')
    success_message = "Company user has been successfully created!"

    def get_context_data(self, **kwargs):
        """
        Add title to context.
        """
        context = super(NewCompanyUser, self).get_context_data(**kwargs)
        context['title'] = self.request.GET.get('title', None)
        context['company'] = self.request.user.company.id
        return context

    def get_initial(self):
        """
        Set initial data.
        """
        return {'company': self.request.user.company,
                'title': self.request.GET.get('title', None)}

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        form.cleaned_data['company'] = self.request.user.company
        form.save()

        return super(NewCompanyUser, self).form_valid(form)

"""
                             LOGS
"""
class ListLogs(ListView):
    """
    List the logs that are generated by AMP.
    """
    queryset = Log.objects.all()
    template_name = 'logs.html'

"""
                             EMPLOYEES
"""
class ListEmployees(ListView):
    """
    List the employees that are owned by the requestors company.
    """
    template_name = 'employees.html'

    def get_queryset(self):
        """
        Refine the queryset.
        """
        return Employee.objects.filter(company=self.request.user.company)

class UpdateEmployee(SuccessMessageMixin, UpdateView):
    """
    Update an employee.
    """
    template_name = 'update_employee.html'
    model = Employee
    success_url = reverse_lazy('employees')
    success_message = "Employee was updated successfully!"

    def get_context_data(self, **kwargs):
        """
        Add some stuff to context.
        """
        context = super(UpdateEmployee, self).get_context_data(**kwargs)
        context['name'] = '%s %s' % (self.get_object().first_name, self.get_object().last_name)
        context['company'] = self.get_object().company.id
        return context

