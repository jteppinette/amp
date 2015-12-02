from app.models import Permission

from django import forms


class NewPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'
        widgets = {
            'company': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewPermissionForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdatePermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        exclude = ('company',)
