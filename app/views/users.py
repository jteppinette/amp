from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse_lazy

from app.forms.users import NewUserForm, UpdateUserForm


class ListUsers(ListView):
    template_name = 'users/list.html'

    def get_queryset(self):
        return get_user_model().objects.filter(company=self.request.user.company)


class NewUser(SuccessMessageMixin, CreateView):
    template_name = 'users/new.html'
    model = get_user_model()
    form_class = NewUserForm
    success_url = reverse_lazy('list-users')
    success_message = '%(title)s %(first_name)s %(last_name)s was successfully created.'

    def get_form_kwargs(self):
        kwargs = super(NewUser, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UpdateUser(SuccessMessageMixin, UpdateView):
    template_name = 'users/update.html'
    model = get_user_model()
    form_class = UpdateUserForm
    success_url = reverse_lazy('list-users')
    success_message = '%(title)s %(first_name)s %(last_name)s was successfully updated.'


class DeleteUser(DeleteView):
    model = get_user_model()
    template_name = 'base/delete.html'
    success_url = reverse_lazy('list-users')
