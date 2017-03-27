"""
Define the views used to render the AMP Contractors pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Contractor, Log


class ListContractors(ListView):
    """
    List the contractors that are owned by the requestors company.
    """
    template_name = 'contractors.html'

    def get_queryset(self):
        """
        Refine the queryset.
        """
        return Contractor.objects.filter(company=self.request.user.company)

class UpdateContractor(SuccessMessageMixin, UpdateView):
    """
    Update an employee.
    """
    template_name = 'update_contractor.html'
    model = Contractor
    success_url = reverse_lazy('contractors')
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
    template_name = 'new_contractor.html'
    model = Contractor
    success_url = reverse_lazy('contractors')
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


def delete_contractor(request, pk):
    """
    Delete a contractor based on pk.
    """
    qs = Contractor.objects.filter(pk=pk)
    if qs:
        qs[0].delete()
        messages.add_message(request, messages.SUCCESS, 'Contractor has been successfully deleted.')
        return redirect('contractors')
    else:
        messages.add_message(request, messages.ERROR, 'Contractor does not exist.')
        return redirect('contractors')


