from app.models import Employee

from django import forms


class NewEmployeeForm(forms.ModelForm):
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
    class Meta:
        model = Employee
        exclude = ('company',)
