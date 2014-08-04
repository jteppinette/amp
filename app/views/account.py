"""
Define the views used to render the AMP Account pages.
"""

from django.views.generic.edit import UpdateView

from django.contrib.messages.views import SuccessMessageMixin

from django.core.urlresolvers import reverse_lazy

from authentication.forms import UserChangeForm

class UpdateAccount(SuccessMessageMixin, UpdateView):
    """
    Update the currently logged in users account.
    """
    template_name = 'update_account.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('update_account')
    success_message = "Your account was updated successfully!"

    def get_object(self, queryset=None):
        """
        Get the object that will be updated.
        """
        return self.request.user



