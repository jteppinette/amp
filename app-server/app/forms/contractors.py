from app.models import Contractor

from django import forms


class NewContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = '__all__'
        widgets = {
            'company': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(NewContractorForm, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company


class UpdateContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        exclude = ('company',)
