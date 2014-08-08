"""
Define the views used to render the AMP Permissions pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DeleteView

from app.utils.views.generic import SearchListView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Permission

from app.forms.permissions import NewPermissionForm, UpdatePermissionForm


class ListPermissions(SearchListView):
    """
    List the permissions that are owned by the requestors company.
    """
    template_name = 'permissions/list.html'
    model = Permission
    search_fields = {'name': 'icontains'}

    def get_queryset(self, *args, **kwargs):
        """
        Filter by company.
        """
        return super(ListPermissions, self).get_queryset(*args, **kwargs).filter(company=self.request.user.company)



class NewPermission(SuccessMessageMixin, CreateView):
    """
    Create a new permission.
    """
    template_name = 'permissions/new.html'
    form_class = NewPermissionForm
    success_url = reverse_lazy('list-permissions')
    success_message = 'Permission "%(name)s" was successfully created.'

    def get_form_kwargs(self):
        kwargs = super(NewPermission, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company.pk})
        return kwargs


class UpdatePermission(SuccessMessageMixin, UpdateView):
    """
    Update a permission.
    """
    template_name = 'permissions/update.html'
    form_class = UpdatePermissionForm
    model = Permission
    success_url = reverse_lazy('list-permissions')
    success_message = 'Permission "%(name)s" was successfully updated.'


class DeletePermission(DeleteView):
    model = Permission
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-permissions')
