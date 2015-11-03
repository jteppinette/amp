"""
Define the forms that will be used by the Employees views.
"""

from api.models import Employee

from django import forms


class NewEmployeeForm(forms.ModelForm):
    """
    This form will be used when a new Employee is being created.
    """
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'company': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdateEmployeeForm(forms.ModelForm):
    """
    This form will be used when an Employee is updated.
    """
    class Meta:
        model = Employee
        exclude = ('company',)
