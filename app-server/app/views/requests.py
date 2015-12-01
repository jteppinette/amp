"""
Define the views used to render the AMP Requests pages.
"""

from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.urlresolvers import reverse_lazy

from app.models import EmployeeRequest, ContractorRequest, Log, Contractor

from app.forms.requests import NewEmployeeRequestForm, NewContractorRequestForm


class NewEmployeeRequest(SuccessMessageMixin, CreateView):
    """
    Create a new employee request.
    """
    template_name = 'requests/new_employee_request.html'
    form_class = NewEmployeeRequestForm
    success_url = reverse_lazy('discover-home')
    success_message = "Employee Request submision was successful. You will be contacted soon."

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save()

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return super(NewEmployeeRequest, self).form_valid(form)


class NewContractorRequest(SuccessMessageMixin, CreateView):
    """
    Create a new contractor request.
    """
    template_name = 'requests/new_contractor_request.html'
    form_class = NewContractorRequestForm
    success_url = reverse_lazy('discover-home')
    success_message = "Contractor Request submision was successful. You will be contacted soon."

    def form_valid(self, form):
        """
        Save the form and generate a proper log.
        """
        obj = form.save(commit=True)

        Log.objects.create(author='Anonymous', **obj.creation_log())

        return super(NewContractorRequest, self).form_valid(form)

def requests(request):
    """
    Load the Employee and Contractor requests into context.
    """
    employee_requests = EmployeeRequest.objects.all().prefetch_related('employee', 'permissions').order_by('employee__first_name')
    contractor_requests = ContractorRequest.objects.all().prefetch_related('permissions').order_by('first_name')

    return render(request, 'requests/list.html', {
        'employee_requests': employee_requests,
        'contractor_requests': contractor_requests,
    })


class DetailEmployeeRequest(DetailView):
    """
    Detail a Request.
    """
    template_name = 'requests/employee_detail.html'
    model = EmployeeRequest


class DetailContractorRequest(DetailView):
    """
    Detail a Request.
    """
    template_name = 'requests/contractor_detail.html'
    model = ContractorRequest


def approve_employee_request(request, pk):
    """
    Approve an employee request based on the provided pk.
    """
    employee_request = EmployeeRequest.objects.get(pk=pk)

    if request.user.title == 'Human Resources':
        employee_request.hr_status = True
    elif request.user.title == 'Training Coordinator':
        employee_request.tc_status = True
    elif request.user.title == 'Access Control Engineer':
        employee_request.ace_status = True

    employee_request.save()

    if request.user.title == 'CIP Manager' or request.user.title == 'Alternate CIP Manager':
        if employee_request.hr_status and employee_request.tc_status and employee_request.ace_status:

            employee = employee_request.employee

            old_permissions = employee.permissions.all()
            length = len(old_permissions)

            employee.permissions.add(*employee_request.permissions.all())
            employee.save()

            Log.objects.create(author=request.user.email, **employee.permission_change_log(old_permissions))

            messages.add_message(request, messages.SUCCESS, "Employee %s %s's request was successfully approved. Permissions have been transferred successfully." % (employee.first_name, employee.last_name))
            employee_request.delete()
            return redirect('list-requests')
   
        else:
            messages.add_message(request, messages.ERROR, "Could not approve final request. Needs approval from: Human Resources, Access Control Engineer, and Training Coordinator.")
            return redirect('detail-employee-request', employee_request.pk)
    else:
        employee = employee_request.employee
        messages.add_message(request, messages.SUCCESS, "Employee %s %s's request has been approved by %s." % (employee.first_name, employee.last_name, request.user.title))
        description = "Employee %s %s's request for %s approved by %s." % (employee.first_name, employee.last_name, employee_request.permissions.all().values_list('name', flat=True), request.user.title)
        Log.objects.create(company=request.user.company, category='Approval', author=request.user.email, accessor='Employee', description=description)
        return redirect('detail-employee-request', employee_request.pk)

def approve_contractor_request(request, pk):
    """
    Approve a contractor request based on the provided pk.
    """
    contractor_request = ContractorRequest.objects.get(pk=pk)

    if request.user.title == 'Human Resources':
        contractor_request.hr_status = True
    elif request.user.title == 'Training Coordinator':
        contractor_request.tc_status = True
    elif request.user.title == 'Access Control Engineer':
        contractor_request.ace_status = True

    contractor_request.save()

    contractor, created = Contractor.objects.get_or_create(
        first_name=contractor_request.first_name,
        last_name=contractor_request.last_name,
        email=contractor_request.email,
        employer=contractor_request.employer,
        company=contractor_request.company
    )
    
    if request.user.title == 'CIP Manager' or request.user.title == 'Alternate CIP Manager':
        if contractor_request.hr_status and contractor_request.tc_status and contractor_request.ace_status:

            old_permissions = contractor.permissions.all()
            length = len(old_permissions)

            contractor.permissions.add(*contractor_request.permissions.all())
            contractor.save()

            Log.objects.create(author=request.user.email, **contractor.permission_change_log(old_permissions))

            messages.add_message(request, messages.SUCCESS, "Contractor %s %s's request was successfully approved. Permissions have been transferred successfully." % (contractor.first_name, contractor.last_name))
            contractor_request.delete()
            return redirect('list-requests')
   
        else:
            messages.add_message(request, messages.ERROR, "Could not approve final request. Needs approval from: Human Resources, Access Control Engineer, and Training Coordinator.")
            return redirect('detail-contractor-request', contractor_request.pk)
    else:
        messages.add_message(request, messages.SUCCESS, "Contractor %s %s's request has been approved by %s." % (contractor.first_name, contractor.last_name, request.user.title))
        description = "Contractor %s %s's request for %s approved by %s." % (contractor.first_name, contractor.last_name, contractor_request.permissions.all().values_list('name', flat=True), request.user.title)
        Log.objects.create(company=request.user.company, category='Approval', author=request.user.email, accessor='Contractor', description=description)
        return redirect('detail-contractor-request', contractor_request.pk)


def reject_employee_request(request, pk):
    """
    Reject a employee request based on the provided pk.
    """
    employee_request = EmployeeRequest.objects.get(pk=pk)
    
    if request.user.title == 'Human Resources':
        employee_request.hr_status = False
    elif request.user.title == 'Training Coordinator':
        employee_request.tc_status = False
    elif request.user.title == 'Access Control Engineer':
        employee_request.ace_status = False

    employee_request.save()
    employee = employee_request.employee

    if request.user.title == 'CIP Manager' or request.user.title == 'Alternate CIP Manager':
        employee_request.cip_status = False
        messages.add_message(request, messages.SUCCESS, "Employee %s %s's request has been rejected and deleted from the system." % (employee.first_name, employee.last_name))
        description = 'Employee %s %s request for %s rejected and deleted from the system.' % (employee.first_name, employee.last_name, employee_request.permissions.all().values_list('name', flat=True))
        Log.objects.create(company=request.user.company, category='Rejection', author=request.user.email, accessor='Employee', description=description)
        employee_request.delete()

        return redirect('list-requests')
    else:
        messages.add_message(request, messages.SUCCESS, "Employee %s %s's request has been rejected by %s." % (employee.first_name, employee.last_name, request.user.title))
        description = 'Employee %s %s request for %s rejected by %s.' % (employee.first_name, employee.last_name, employee_request.permissions.all().values_list('name', flat=True), request.user.title)
        Log.objects.create(company=request.user.company, category='Rejection', author=request.user.email, accessor='Employee', description=description)

        return redirect('detail-employee-request', employee_request.pk)

def reject_contractor_request(request, pk):
    """
    Reject a contractor request based on the provided pk.
    """
    contractor_request = ContractorRequest.objects.get(pk=pk)
    
    if request.user.title == 'Human Resources':
        contractor_request.hr_status = False
    elif request.user.title == 'Training Coordinator':
        contractor_request.tc_status = False
    elif request.user.title == 'Access Control Engineer':
        contractor_request.ace_status = False

    contractor_request.save()
    contractor, created = Contractor.objects.get_or_create(
        first_name=contractor_request.first_name,
        last_name=contractor_request.last_name,
        email=contractor_request.email,
        employer=contractor_request.employer,
        company=contractor_request.company
    )

    if request.user.title == 'CIP Manager' or request.user.title == 'Alternate CIP Manager':
        contractor_request.cip_status = False
        messages.add_message(request, messages.SUCCESS, "Contractor %s %s's request has been rejected and deleted from the system." % (contractor.first_name, contractor.last_name))
        description = "Contractor %s %s's request for %s rejected and deleted from the system." % (contractor.first_name, contractor.last_name, contractor_request.permissions.all().values_list('name', flat=True))
        Log.objects.create(company=request.user.company, category='Rejection', author=request.user.email, accessor='Contractor', description=description)
        contractor_request.delete()

        return redirect('list-requests')
    else:
        messages.add_message(request, messages.SUCCESS, "Contractor %s %s's request has been rejected by %s." % (contractor.first_name, contractor.last_name, request.user.title))
        description = "Contractor %s %s's request for %s rejected by %s." % (contractor.first_name, contractor.last_name, contractor_request.permissions.all().values_list('name', flat=True), request.user.title)
        Log.objects.create(company=request.user.company, category='Rejection', author=request.user.email, accessor='Contractor', description=description)

        return redirect('detail-contractor-request', contractor_request.pk)

