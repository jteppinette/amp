from app.models import EmployeeRequest, ContractorRequest

from django import forms


class NewEmployeeRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeRequest
        exclude = ('hr_status', 'tc_status', 'ace_status', 'cip_status')


class NewContractorRequestForm(forms.ModelForm):
    class Meta:
        model = ContractorRequest
        exclude = ('hr_status', 'tc_status', 'ace_status', 'cip_status')
