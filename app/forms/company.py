"""
Define the forms that will be used by the Company views.
"""

from bootstrapforms.forms import BootstrapModelForm

from api.models import Company
from authentication.models import User

from django import forms


class NewCompanyUserForm(BootstrapModelForm):
    """
    This form will be used when a new Company User is being created.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'company', 'title')
        widgets = {
            'company': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewCompanyUserForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company

    def clean_password2(self):
        """
        Check that the two password entries match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Password do not match.')
        
        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format.
        """
        user = super(NewCompanyUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UpdateCompanyUserForm(BootstrapModelForm):
    """
    This form will be used when a Company User is updated.
    """
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'title')

    def save(self, commit=True):
        """
        Save the form and if the user has provided a new password, set it.

        Additionally, provide support for a user to have commit set to
        `False` and not save the created object.
        """
        user = super(UpdateCompanyUserForm, self).save(commit=False)
        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()

        return user
