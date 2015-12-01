"""
Define the forms that will be used by the Settings views.
"""

from app.models import Company

from django import forms


class UpdateSettingsForm(forms.ModelForm):
    """
    This form will be used when updating the currently logged in user's settings.
    """

    class Meta:
        model = Company
        fields = '__all__'
