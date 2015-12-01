from app.models import EmployeeDocument, ContractorDocument

from django import forms


class NewEmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = '__all__'
        widgets = {
            'employee': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        employee = kwargs.pop('employee')
        super(NewEmployeeDocumentForm, self).__init__(*args, **kwargs)
        self.fields['employee'].initial = employee


class NewContractorDocumentForm(forms.ModelForm):
    class Meta:
        model = ContractorDocument
        fields = '__all__'
        widgets = {
            'contractor': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        contractor = kwargs.pop('contractor')
        super(NewContractorDocumentForm, self).__init__(*args, **kwargs)
        self.fields['contractor'].initial = contractor
