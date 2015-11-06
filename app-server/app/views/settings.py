"""
Define the views used to render the AMP Settings pages.
"""

from django.views.generic.edit import UpdateView

from django.contrib.messages.views import SuccessMessageMixin

from django.core.urlresolvers import reverse_lazy

from app.forms.settings import UpdateSettingsForm


class UpdateSettings(SuccessMessageMixin, UpdateView):
    """
    Update the currently logged in users account.
    """
    template_name = 'settings/update.html'
    form_class = UpdateSettingsForm
    success_url = reverse_lazy('update-settings')
    success_message = "Your settings were successfully updated."

    def get_object(self, queryset=None):
        """
        Get the object that will be updated.
        """
        return self.request.user.company
