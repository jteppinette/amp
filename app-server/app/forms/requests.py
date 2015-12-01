"""
Define the forms that will be used by the Requests views.
"""

from app.models import EmployeeRequest, ContractorRequest

from django import forms


class NewEmployeeRequestForm(forms.ModelForm):
    """
    The form that will be used a new request is made by an Employee.
    """
    class Meta:
        model = EmployeeRequest
        exclude = ('hr_status', 'tc_status', 'ace_status', 'cip_status')


class NewContractorRequestForm(forms.ModelForm):
    """
    The form that will be used a new request is made by a Contractor.
    """
    class Meta:
        model = ContractorRequest
        exclude = ('hr_status', 'tc_status', 'ace_status', 'cip_status')
