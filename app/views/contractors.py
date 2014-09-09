"""
Define the views used to render the AMP Contractors pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DeleteView

from app.utils.views.generic import SearchListView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Contractor, Log

from app.forms.contractors import NewContractorForm, UpdateContractorForm


class ListContractors(SearchListView):
    """
    List the contractors that are owned by the requestors company.
    """
    template_name = 'contractors/list.html'
    model = Contractor
    search_fields = {'first_name': 'icontains', 'last_name': 'icontains'}

    def get_queryset(self, *args, **kwargs):
        """
        Refine by company.
        """
        orderby = self.request.GET.get('orderby', None)
        qs = super(ListContractors, self).get_queryset(*args, **kwargs).filter(company=self.request.user.company)
        if orderby is None or orderby == '':
            return qs
        else:
            return qs.order_by(orderby)
        
    def get_context_data(self, *args, **kwargs):
        context = super(ListContractors, self).get_context_data(*args, **kwargs)
        context['options'] = [
            {'value': 'first_name', 'name': 'First Name'},
            {'value': 'last_name', 'name': 'Last Name'},
            {'value': 'last_training_date', 'name': 'Training Due Date'},
            {'value': 'last_background_check_date', 'name': 'Background Due Date'},
        ]
        context['orderby'] = self.request.GET.get('orderby', None)
        return context


class NewContractor(SuccessMessageMixin, CreateView):
    """
    Create a new contractor.
    """
    template_name = 'contractors/new.html'
    form_class = NewContractorForm
    success_url = reverse_lazy('list-contractors')
    success_message = 'Contractor %(first_name)s %(last_name)s was successfully created.'

    def get_form_kwargs(self):
        kwargs = super(NewContractor, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company.pk})
        return kwargs

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save(commit=True)
        Log.objects.create(author=self.request.user.email, **obj.creation_log())
        return super(NewContractor, self).form_valid(form)


class UpdateContractor(SuccessMessageMixin, UpdateView):
    """
    Update an employee.
    """
    template_name = 'contractors/update.html'
    form_class = UpdateContractorForm
    model = Contractor
    success_url = reverse_lazy('list-contractors')
    success_message = 'Contractor %(first_name)s %(last_name)s was successfully updated.'

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        old_permissions = self.object.permissions.all()
        length = len(old_permissions)

        obj = form.save()
        Log.objects.create(author=self.request.user.email, **self.object.permission_change_log(old_permissions))
        return super(UpdateContractor, self).form_valid(form)


class DeleteContractor(DeleteView):
    model = Contractor
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-contractors')
