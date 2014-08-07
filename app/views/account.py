"""
Define the views used to render the AMP Account pages.
"""

from django.views.generic.edit import UpdateView

from django.contrib.messages.views import SuccessMessageMixin

from django.core.urlresolvers import reverse_lazy

from app.forms.account import UpdateAccountForm


class UpdateAccount(SuccessMessageMixin, UpdateView):
    """
    Update the currently logged in users account.
    """
    template_name = 'account/update.html'
    form_class = UpdateAccountForm
    success_url = reverse_lazy('update-account')
    success_message = "Your account was successfully updated."

    def get_object(self, queryset=None):
        """
        Get the object that will be updated.
        """
        return self.request.user
