"""
Define the forms that will be used by the Employees views.
"""

from bootstrapforms.forms import BootstrapModelForm

from api.models import Employee

from django.forms import HiddenInput


class NewEmployeeForm(BootstrapModelForm):
    """
    This form will be used when a new Employee is being created.
    """
    class Meta:
        model = Employee
        widgets = {
            'company': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdateEmployeeForm(BootstrapModelForm):
    """
    This form will be used when an Employee is updated.
    """
    class Meta:
        model = Employee
        exclude = ('company',)
