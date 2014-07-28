"""
This module defines the forms required for the new `User` model to take
take advantage of Django's User system, specifically the admin site.
"""

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authentication.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all required fields, plus a
    repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'company', 'title')

    def clean_password2(self):
        """
        Check that the two password entries match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    new_password = forms.CharField(widget=forms.PasswordInput,
                                   required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin', 'first_name', 'last_name', 'company', 'title')

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the field does
        not have access to the initial value.
        """
        return self.initial['password']

    def clean_is_admin(self):
        """
        If nothing is passed, return the initial value.
        """
        if self.cleaned_data['is_admin']:
            return self.cleaned_data['is_admin']
        else:
            return self.initial['is_admin']

    def clean_is_active(self):
        """
        If nothin is passed, return the initial value.
        """
        if self.cleaned_data['is_active']:
            return self.cleaned_data['is_active']
        else:
            return self.initial['is_active']

    def save(self, commit=True):
        """
        Save the form and if the user has provided a new password, set it.

        Additionally, provide support for a user to have commit set to
        `False` and not save the created object.
        """
        user = super(UserChangeForm, self).save(commit=False)
        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()

        return user
    
