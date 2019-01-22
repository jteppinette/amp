from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from amp.models import (
    PROFILE_TITLES,
    Contractor,
    ContractorDocument,
    ContractorRequest,
    Employee,
    EmployeeDocument,
    EmployeeRequest,
    Permission,
    Profile,
)


class AccountGeneralUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")


class NewContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = "__all__"


class UpdateContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = "__all__"


class NewEmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = "__all__"
        widgets = {"employee": forms.HiddenInput()}


class NewContractorDocumentForm(forms.ModelForm):
    class Meta:
        model = ContractorDocument
        fields = "__all__"
        widgets = {"contractor": forms.HiddenInput()}


class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


class UpdateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


class NewPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = "__all__"


class UpdatePermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = "__all__"


class NewEmployeeRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeRequest
        exclude = ("hr_status", "tc_status", "ace_status", "cip_status")


class NewContractorRequestForm(forms.ModelForm):
    class Meta:
        model = ContractorRequest
        exclude = ("hr_status", "tc_status", "ace_status", "cip_status")


class NewUserForm(UserCreationForm):
    title = forms.ChoiceField(choices=PROFILE_TITLES, required=True)

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Profile.objects.update_or_create(
                user=user, defaults={"title": self.cleaned_data["title"]}
            )
        return user


class UpdateUserForm(UserChangeForm):
    title = forms.ChoiceField(choices=PROFILE_TITLES, required=True)

    class Meta(UserChangeForm.Meta):
        exclude = (
            "user_permissions",
            "groups",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "password1",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Profile.objects.update_or_create(
                user=user, defaults={"title": self.cleaned_data["title"]}
            )
        return user
