from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView
from django.views.generic import DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from app.models import Employee, EmployeeDocument

from app.forms.documents import NewEmployeeDocumentForm


class NewEmployeeDocument(SuccessMessageMixin, CreateView):
    template_name = 'documents/new_employee_document.html'
    form_class = NewEmployeeDocumentForm
    success_message = "Employee Document was successfully created."

    def get_success_url(self):
        return reverse_lazy('update-employee', args=[self.kwargs.get('employee', None)])

    def get_context_data(self, **kwargs):
        kwargs.setdefault('employee', Employee.objects.get(id=self.kwargs.get('employee', None)))
        return super(NewEmployeeDocument, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(NewEmployeeDocument, self).get_form_kwargs()
        kwargs.update({'employee': self.kwargs.get('employee', None)})
        return kwargs


class DeleteEmployeeDocument(DeleteView):
    model = EmployeeDocument
    template_name = 'base/delete.html'

    def get_success_url(self):
        return reverse_lazy('update-employee', args=[self.kwargs.get('employee', None)])
