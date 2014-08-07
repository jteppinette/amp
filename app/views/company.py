"""
Define the views used to render the AMP Company pages.
"""

from authentication.forms import UserChangeForm, UserCreationForm

from django.shortcuts import redirect, render

from django.views.generic.edit import UpdateView, CreateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse_lazy

from app.forms.company import NewCompanyUserForm, UpdateCompanyUserForm

def company(request):
    """
    Show the four other users in the CIP Manager's company.
    """
    if request.user.title != 'CIP Manager':
        return redirect('dashboard-home')

    company = request.user.company

    obj_mng = get_user_model().objects
    
    qs = obj_mng.filter(company=company, title='Alternate CIP Manager')
    if qs:
        alternate_cip_manager = qs[0]
    else:
        alternate_cip_manager = None
    qs = obj_mng.filter(company=company, title='Access Control Engineer')
    if qs:
        access_control_engineer = qs[0]
    else:
        access_control_engineer = None
    qs = obj_mng.filter(company=company, title='Training Coordinator')
    if qs:
        training_coordinator = qs[0]
    else:
        training_coordinator = None
    qs = obj_mng.filter(company=company, title='Human Resources')
    if qs:
        human_resources = qs[0]
    else:
        human_resources = None

    return render(request, 'company/list.html', {
        'alternate_cip_manager': alternate_cip_manager,
        'access_control_engineer': access_control_engineer,
        'training_coordinator': training_coordinator,
        'human_resources': human_resources,
    })

class NewCompanyUser(SuccessMessageMixin, CreateView):
    """
    Create a new contractor request.
    """
    template_name = 'company/new.html'
    model = get_user_model()
    form_class = NewCompanyUserForm
    success_url = reverse_lazy('list-company-users')
    success_message = "Company user has been successfully created!"

    def get_form_kwargs(self):
        kwargs = super(NewCompanyUser, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company})
        return kwargs


class UpdateCompanyUser(SuccessMessageMixin, UpdateView):
    """
    Update a company user.
    """
    template_name = 'company/update.html'
    model = get_user_model()
    form_class = UpdateCompanyUserForm
    success_url = reverse_lazy('list-company-users')
    success_message = "Company user was updated successfuly!"
