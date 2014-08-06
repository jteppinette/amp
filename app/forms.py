"""
Define the forms that will be used in the AMP app.
"""

from bootstrapforms.forms import BootstrapModelForm

from api.models import EmployeeRequest, ContractorRequest

class NewEmployeeRequestForm(BootstrapModelForm):
    """
    The form that will be used a new request is made by an Employee.
    """
    class Meta:
        model = EmployeeRequest


class NewContractorRequestForm(BootstrapModelForm):
    """
    The form that will be used a new request is made by a Contractor.
    """
    class Meta:
        model = ContractorRequest
