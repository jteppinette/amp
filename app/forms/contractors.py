"""
Define the forms that will be used by the Contractors views.
"""

from bootstrapforms.forms import BootstrapModelForm

from api.models import Contractor

from django.forms import HiddenInput


class NewContractorForm(BootstrapModelForm):
    """
    This form will be used when a new Contractor is being created.
    """
    class Meta:
        model = Contractor
        widgets = {
            'company': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewContractorForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdateContractorForm(BootstrapModelForm):
    """
    This form will be used when a Contractor is updated.
    """
    class Meta:
        model = Contractor
        exclude = ('company',)
