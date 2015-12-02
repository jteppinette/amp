from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authentication.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'company', 'title')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    new_password = forms.CharField(widget=forms.PasswordInput,
                                   required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin', 'first_name', 'last_name', 'company', 'title')

    def clean_password(self):
        return self.initial['password']

    def clean_is_admin(self):
        if self.cleaned_data['is_admin']:
            return self.cleaned_data['is_admin']
        else:
            return self.initial['is_admin']

    def clean_is_active(self):
        if self.cleaned_data['is_active']:
            return self.cleaned_data['is_active']
        else:
            return self.initial['is_active']

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()

        return user
