from app.models import Company

from django import forms


class UpdateSettingsForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
