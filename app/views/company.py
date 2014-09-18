"""
Define the views used to render the AMP Company pages.
"""

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse_lazy

from app.forms.company import NewCompanyUserForm, UpdateCompanyUserForm


class ListCompanyUsers(ListView):
    """
    List the company users that are owned by the requestors company.
    """
    template_name = 'company/list.html'

    def get_queryset(self):
        return get_user_model().objects.filter(company=self.request.user.company)


class NewCompanyUser(SuccessMessageMixin, CreateView):
    """
    Create a new contractor request.
    """
    template_name = 'company/new.html'
    model = get_user_model()
    form_class = NewCompanyUserForm
    success_url = reverse_lazy('list-company-users')
    success_message = '%(title)s %(first_name)s %(last_name)s was successfully created.'

    def get_form_kwargs(self):
        kwargs = super(NewCompanyUser, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UpdateCompanyUser(SuccessMessageMixin, UpdateView):
    """
    Update a company user.
    """
    template_name = 'company/update.html'
    model = get_user_model()
    form_class = UpdateCompanyUserForm
    success_url = reverse_lazy('list-company-users')
    success_message = '%(title)s %(first_name)s %(last_name)s was successfully updated.'


class DeleteCompanyUser(DeleteView):
    model = get_user_model()
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-company-users')
