from app.models import EmployeeDocument

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
