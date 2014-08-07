"""
Define the forms that will be used by the Account views.
"""

from bootstrapforms.forms import BootstrapModelForm

from authentication.models import User

from django import forms


class UpdateAccountForm(BootstrapModelForm):
    """
    This form will be used when updating the currently logged in user' account.
    """
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'title')

    def __init__(self, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['title'].required = True

    def save(self, commit=True):
        """
        Save the form and if the user has provided a new password, set it.

        Additionally, provide support for a user to have commit set to
        `False` and not save the created object.
        """
        user = super(UpdateAccountForm, self).save(commit=False)
        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()

        return user
