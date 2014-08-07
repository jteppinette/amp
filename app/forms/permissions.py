"""
Define the forms that will be used by the Permissions views.
"""

from bootstrapforms.forms import BootstrapModelForm

from api.models import Permission

from django.forms import HiddenInput


class NewPermissionForm(BootstrapModelForm):
    """
    This form will be used when a new Permission is being created.
    """
    class Meta:
        model = Permission
        widgets = {
            'company': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewPermissionForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdatePermissionForm(BootstrapModelForm):
    """
    This form will be used when a Permission is updated.
    """
    class Meta:
        model = Permission
        exclude = ('company',)
