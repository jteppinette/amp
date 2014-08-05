"""
Define the forms that will be used in the AMP app.
"""

from django import forms

from api.models import EmployeeRequest, ContractorRequest

class NewEmployeeRequestForm(forms.ModelForm):
    """
    The form that will be used a new request is made by an Employee.
    """
    class Meta:
        model = EmployeeRequest

    def __init__(self, *args, **kwargs):
        """
        Manipulate the fields widgets.
        """
        super(NewEmployeeRequestForm, self).__init__(*args, **kwargs)
        
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

class NewContractorRequestForm(forms.ModelForm):
    """
    The form that will be used a new request is made by a Contractor.
    """
    class Meta:
        model = ContractorRequest

    def __init__(self, *args, **kwargs):
        """
        Manipulate the fields widgets.
        """
        super(NewContractorRequestForm, self).__init__(*args, **kwargs)
        
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})

        self.fields['background_check'].widget.attrs.update({'class': ''})
        self.fields['remote'].widget.attrs.update({'class': ''}) 
