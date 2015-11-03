"""
Define the forms that will be used by the Permissions views.
"""

from api.models import Permission

from django import forms


class NewPermissionForm(forms.ModelForm):
    """
    This form will be used when a new Permission is being created.
    """
    class Meta:
        model = Permission
        fields = '__all__'
        widgets = {
            'company': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewPermissionForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdatePermissionForm(forms.ModelForm):
    """
    This form will be used when a Permission is updated.
    """
    class Meta:
        model = Permission
        exclude = ('company',)
