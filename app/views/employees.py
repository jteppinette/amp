"""
Define the views used to render the AMP Employees pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Employee, Log

from app.forms.employees import NewEmployeeForm, UpdateEmployeeForm


class ListEmployees(ListView):
    """
    List the employees that are owned by the requestors company.
    """
    template_name = 'employees/list.html'

    def get_queryset(self):
        """
        Refine the queryset.
        """
        return Employee.objects.filter(company=self.request.user.company)


class NewEmployee(SuccessMessageMixin, CreateView):
    """
    Create a new employee.
    """
    template_name = 'employees/new.html'
    form_class = NewEmployeeForm
    success_url = reverse_lazy('list-employees')
    success_message = 'Employee %(first_name)s %(last_name)s was successfully created.'

    def get_form_kwargs(self):
        kwargs = super(NewEmployee, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company.pk})
        return kwargs

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save()
        Log.objects.create(author=self.request.user.email, **obj.creation_log())
        return super(NewEmployee, self).form_valid(form)


class UpdateEmployee(SuccessMessageMixin, UpdateView):
    """
    Update an employee.
    """
    template_name = 'employees/update.html'
    form_class = UpdateEmployeeForm
    model = Employee
    success_url = reverse_lazy('list-employees')
    success_message = 'Employee %(first_name)s %(last_name)s was successfully updated.'


class DeleteEmployee(DeleteView):
    model = Employee
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-employees')
