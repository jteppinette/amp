"""
Define the views used to render the AMP Employees pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Employee, Log


class ListEmployees(ListView):
    """
    List the employees that are owned by the requestors company.
    """
    template_name = 'employees/employees.html'

    def get_queryset(self):
        """
        Refine the queryset.
        """
        return Employee.objects.filter(company=self.request.user.company)

class UpdateEmployee(SuccessMessageMixin, UpdateView):
    """
    Update an employee.
    """
    template_name = 'employees/update_employee.html'
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

class NewEmployee(SuccessMessageMixin, CreateView):
    """
    Create a new employee.
    """
    template_name = 'employees/new_employee.html'
    model = Employee
    success_url = reverse_lazy('employees')
    success_message = "Employee creation was a success!"

    def get_context_data(self, **kwargs):
        """
        Add some stuff to context.
        """
        context = super(NewEmployee, self).get_context_data(**kwargs)
        context['company'] = self.request.user.company.id
        return context

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save(commit=True)

        Log.objects.create(author=self.request.user.email, **obj.creation_log())

        return super(NewEmployee, self).form_valid(form)

def delete_employee(request, pk):
    """
    Delete an employee based on pk.
    """
    qs = Employee.objects.filter(pk=pk)
    if qs:
        qs[0].delete()
        messages.add_message(request, messages.SUCCESS, 'Employee has been successfully deleted.')
        return redirect('employees')
    else:
        messages.add_message(request, messages.ERROR, 'Employee does not exist.')
        return redirect('employees')
