"""
Define the views used to render the AMP Requests pages.
"""

from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import EmployeeRequest, ContractorRequest, Log

from app.forms.requests import NewEmployeeRequestForm, NewContractorRequestForm


class NewEmployeeRequest(SuccessMessageMixin, CreateView):
    """
    Create a new employee request.
    """
    template_name = 'requests/new_employee_request.html'
    form_class = NewEmployeeRequestForm
    success_url = reverse_lazy('discover-home')
    success_message = "Employee Request submision was successful. You will be contacted soon."

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
    template_name = 'requests/new_contractor_request.html'
    form_class = NewContractorRequestForm
    success_url = reverse_lazy('discover-home')
    success_message = "Contractor Request submision was successful. You will be contacted soon."

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save(commit=True)

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return super(NewContractorRequest, self).form_valid(form)

def requests(request):
    """
    Load the Employee and Contractor requests into context.
    """
    employee_requests = EmployeeRequest.objects.all().prefetch_related('employee', 'permissions')
    contractor_requests = ContractorRequest.objects.all().prefetch_related('permissions')

    return render(request, 'requests/list.html', {
        'employee_requests': employee_requests,
        'contractor_requests': contractor_requests,
    })

def approve_employee_request(request, pk):
    """
    Approve an employee request based on the provided pk.
    """
    employee_request = EmployeeRequest.objects.get(pk=pk)
    employee = employee_request.employee

    old_permissions = employee.permissions.all()
    length = len(old_permissions)

    employee.permissions.add(*employee_request.permissions.all())
    employee.save()

    employee_request.delete()

    Log.objects.create(author=request.user.email, **employee.permission_change_log(old_permissions))

    messages.add_message(request, messages.SUCCESS, "Employee %s %s's request was successfully approved." % (employee.first_name, employee.last_name))
    return redirect('list-requests')
