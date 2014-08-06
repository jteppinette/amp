"""
Define the views used to render the AMP Permissions pages.
"""

from django.shortcuts import redirect

from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from api.models import Permission


class ListPermissions(ListView):
    """
    List the permissions that are owned by the requestors company.
    """
    template_name = 'permissions/list.html'

    def get_queryset(self):
        """
        Refine the queryset.
        """
        return Permission.objects.filter(company=self.request.user.company)


class UpdatePermission(SuccessMessageMixin, UpdateView):
    """
    Update a permission.
    """
    template_name = 'permissions/update.html'
    model = Permission
    success_url = reverse_lazy('list-permissions')
    success_message = "Permission was updated successfully!"

    def get_context_data(self, **kwargs):
        """
        Add some stuff to context.
        """
        context = super(UpdatePermission, self).get_context_data(**kwargs)
        context['name'] = self.get_object().name
        context['company'] = self.get_object().company.id
        return context

class NewPermission(SuccessMessageMixin, CreateView):
    """
    Create a new permission.
    """
    template_name = 'permissions/new.html'
    model = Permission
    success_url = reverse_lazy('list-permissions')
    success_message = "Permissions creation was a success!"

    def get_context_data(self, **kwargs):
        """
        Add some stuff to context.
        """
        context = super(NewPermission, self).get_context_data(**kwargs)
        context['company'] = self.request.user.company.id
        return context

class DeletePermission(DeleteView):
    model = Permission
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-permissions')
