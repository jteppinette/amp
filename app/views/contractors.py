"""
Define the views used to render the AMP Contractors pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Contractor, Log


class ListContractors(ListView):
    """
    List the contractors that are owned by the requestors company.
    """
    template_name = 'contractors/list.html'

    def get_queryset(self):
        """
        Refine the queryset.
        """
        return Contractor.objects.filter(company=self.request.user.company)

class UpdateContractor(SuccessMessageMixin, UpdateView):
    """
    Update an employee.
    """
    template_name = 'contractors/update.html'
    model = Contractor
    success_url = reverse_lazy('list-contractors')
    success_message = "Contractor was updated successfully!"

    def get_context_data(self, **kwargs):
        """
        Add some stuff to context.
        """
        context = super(UpdateContractor, self).get_context_data(**kwargs)
        context['name'] = '%s %s' % (self.get_object().first_name, self.get_object().last_name)
        context['company'] = self.get_object().company.id
        return context

class NewContractor(SuccessMessageMixin, CreateView):
    """
    Create a new contractor.
    """
    template_name = 'contractors/new.html'
    model = Contractor
    success_url = reverse_lazy('list-contractors')
    success_message = "Contractor creation was a success!"

    def get_context_data(self, **kwargs):
        """
        Add some stuff to context.
        """
        context = super(NewContractor, self).get_context_data(**kwargs)
        context['company'] = self.request.user.company.id
        return context

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save(commit=True)

        Log.objects.create(author=self.request.user.email, **obj.creation_log())

        return super(NewContractor, self).form_valid(form)


class DeleteContractor(DeleteView):
    model = Contractor
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-contractors')
