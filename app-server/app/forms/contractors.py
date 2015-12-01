"""
Define the forms that will be used by the Contractors views.
"""

from app.models import Contractor

from django import forms


class NewContractorForm(forms.ModelForm):
    """
    This form will be used when a new Contractor is being created.
    """
    class Meta:
        model = Contractor
        fields = '__all__'
        widgets = {
            'company': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewContractorForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdateContractorForm(forms.ModelForm):
    """
    This form will be used when a Contractor is updated.
    """
    class Meta:
        model = Contractor
        exclude = ('company',)
