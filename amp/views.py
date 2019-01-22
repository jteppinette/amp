from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView

from amp.forms import (
    AccountGeneralUpdateForm,
    NewContractorDocumentForm,
    NewContractorForm,
    NewContractorRequestForm,
    NewEmployeeDocumentForm,
    NewEmployeeForm,
    NewEmployeeRequestForm,
    NewPermissionForm,
    NewUserForm,
    UpdateContractorForm,
    UpdateEmployeeForm,
    UpdatePermissionForm,
    UpdateUserForm,
)
from amp.models import (
    LOG_CATEGORIES,
    Contractor,
    ContractorDocument,
    ContractorRequest,
    Employee,
    EmployeeDocument,
    EmployeeRequest,
    Log,
    Permission,
)
from amp.utils.views import SearchCSVView, SearchListView


class Landing(TemplateView):
    template_name = "landing.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")

        return super().get(request, *args, **kwargs)


class Dashboard(TemplateView):
    template_name = "dashboard.html"


class AccountGeneralUpdate(SuccessMessageMixin, UpdateView):
    template_name = "account/general/update.html"
    form_class = AccountGeneralUpdateForm
    success_url = reverse_lazy("dashboard")
    success_message = "Your account was successfully updated."

    def get_object(self):
        return self.request.user


class AccountPasswordChange(SuccessMessageMixin, PasswordChangeView):
    template_name = "account/password/change.html"
    success_url = reverse_lazy("dashboard")
    success_message = "Your password was successfully changed."


class ListContractors(SearchListView):
    paginate_by = 20
    template_name = "contractors/list.html"
    queryset = Contractor.objects.all()
    search_fields = {"first_name": "icontains", "last_name": "icontains"}

    def get(self, request, *args, **kwargs):
        self.orderby = request.GET.get("orderby")
        return super().get(request, *args, **kwargs)

    def get_ordering(self):
        return self.orderby

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["options"] = [
            {"value": "first_name", "name": "First Name"},
            {"value": "last_name", "name": "Last Name"},
            {"value": "last_training_date", "name": "Training Due Date"},
            {"value": "last_background_check_date", "name": "Background Due Date"},
        ]
        context["orderby"] = self.orderby
        return context


class CSVContractors(SearchCSVView):
    queryset = Contractor.objects.all()
    search_fields = {"first_name": "icontains", "last_name": "icontains"}

    def get(self, request, *args, **kwargs):
        self.orderby = request.GET.get("orderby")
        return super().get(request, *args, **kwargs)

    def get_ordering(self):
        return self.orderby


class NewContractor(SuccessMessageMixin, CreateView):
    template_name = "contractors/new.html"
    form_class = NewContractorForm
    success_url = reverse_lazy("list-contractors")
    success_message = "Contractor %(first_name)s %(last_name)s was successfully created."

    def form_valid(self, form):
        contractor = form.save(commit=False)
        Log.objects.create(author=self.request.user.email, **contractor.creation_log())
        return super().form_valid(form)


class UpdateContractor(SuccessMessageMixin, UpdateView):
    template_name = "contractors/update.html"
    form_class = UpdateContractorForm
    queryset = Contractor.objects.all()
    success_url = reverse_lazy("list-contractors")
    success_message = "Contractor %(first_name)s %(last_name)s was successfully updated."
    pk_url_kwarg = "contractor_pk"

    def form_valid(self, form):
        old_permissions = self.object.permissions.all()
        contractor = form.save(commit=False)
        Log.objects.create(
            author=self.request.user.email, **contractor.permission_change_log(old_permissions)
        )
        return super().form_valid(form)


class DeleteContractor(DeleteView):
    model = Contractor
    template_name = "delete.html"
    success_url = reverse_lazy("list-contractors")
    pk_url_kwarg = "contractor_pk"


class NewEmployeeDocument(SuccessMessageMixin, CreateView):
    template_name = "documents/new_employee_document.html"
    form_class = NewEmployeeDocumentForm
    success_message = "Employee Document was successfully created."

    def get(self, request, employee_pk, *args, **kwargs):
        self.employee = get_object_or_404(Employee, pk=employee_pk)
        return super().get(request, employee_pk, *args, **kwargs)

    def post(self, request, employee_pk, *args, **kwargs):
        self.employee = get_object_or_404(Employee, pk=employee_pk)
        return super().post(request, employee_pk, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("update-employee", args=[self.employee.pk])

    def get_initial(self):
        initial = super().get_initial()
        initial["employee"] = self.employee
        return initial


class DeleteEmployeeDocument(DeleteView):
    model = EmployeeDocument
    template_name = "delete.html"
    pk_url_kwarg = "document_pk"

    def get_success_url(self):
        return reverse_lazy("update-employee", args=[self.object.id])


class NewContractorDocument(SuccessMessageMixin, CreateView):
    template_name = "documents/new_contractor_document.html"
    form_class = NewContractorDocumentForm
    success_message = "Contractor Document was successfully created."

    def get(self, request, contractor_pk, *args, **kwargs):
        self.contractor = get_object_or_404(Contractor, pk=contractor_pk)
        return super().get(request, contractor_pk, *args, **kwargs)

    def post(self, request, contractor_pk, *args, **kwargs):
        self.contractor = get_object_or_404(Contractor, pk=contractor_pk)
        return super().post(request, contractor_pk, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("update-contractor", args=[self.contractor.pk])

    def get_initial(self):
        initial = super().get_initial()
        initial["contractor"] = self.contractor
        return initial


class DeleteContractorDocument(DeleteView):
    model = ContractorDocument
    template_name = "delete.html"
    pk_url_kwarg = "document_pk"

    def get_success_url(self):
        return reverse_lazy("update-contractor", args=[self.object.contractor_id])


class ListEmployees(SearchListView):
    paginate_by = 20
    template_name = "employees/list.html"
    queryset = Employee.objects.all()
    search_fields = {"first_name": "icontains", "last_name": "icontains"}

    def get(self, request, *args, **kwargs):
        self.orderby = request.GET.get("orderby")
        return super().get(request, *args, **kwargs)

    def get_ordering(self):
        return self.orderby

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["options"] = [
            {"value": "first_name", "name": "First Name"},
            {"value": "last_name", "name": "Last Name"},
            {"value": "last_training_date", "name": "Training Due Date"},
            {"value": "last_background_check_date", "name": "Background Due Date"},
        ]
        context["orderby"] = self.orderby
        return context


class CSVEmployees(SearchCSVView):
    queryset = Employee.objects.all()
    search_fields = {"first_name": "icontains", "last_name": "icontains"}

    def get(self, request, *args, **kwargs):
        self.orderby = request.GET.get("orderby")
        return super().get(request, *args, **kwargs)

    def get_ordering(self):
        return self.orderby


class NewEmployee(SuccessMessageMixin, CreateView):
    template_name = "employees/new.html"
    form_class = NewEmployeeForm
    success_url = reverse_lazy("list-employees")
    success_message = "Employee %(first_name)s %(last_name)s was successfully created."

    def form_valid(self, form):
        employee = form.save(commit=False)
        Log.objects.create(author=self.request.user.email, **employee.creation_log())
        return super().form_valid(form)


class UpdateEmployee(SuccessMessageMixin, UpdateView):
    template_name = "employees/update.html"
    form_class = UpdateEmployeeForm
    queryset = Employee.objects.all()
    success_url = reverse_lazy("list-employees")
    success_message = "Employee %(first_name)s %(last_name)s was successfully updated."
    pk_url_kwarg = "employee_pk"

    def form_valid(self, form):
        old_permissions = self.object.permissions.all()

        employee = form.save(commit=False)
        Log.objects.create(
            author=self.request.user.email, **employee.permission_change_log(old_permissions)
        )
        return super().form_valid(form)


class DeleteEmployee(DeleteView):
    queryset = Employee.objects.all()
    template_name = "delete.html"
    success_url = reverse_lazy("list-employees")
    pk_url_kwarg = "employee_pk"


class ListLogs(SearchListView):
    queryset = Log.objects.all()
    paginate_by = 20
    template_name = "logs/list.html"
    search_fields = {"category": "exact", "author": "icontains", "accessor": "icontains"}
    ordering = "-creation_time"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = LOG_CATEGORIES
        return context


class CSVLogs(SearchCSVView):
    queryset = Log.objects.all()
    search_fields = {"category": "exact", "author": "icontains", "accessor": "icontains"}
    ordering = "-creation_time"


class ListPermissions(SearchListView):
    paginate_by = 20
    template_name = "permissions/list.html"
    queryset = Permission.objects.all()
    search_fields = {"name": "icontains"}


class CSVPermissions(SearchCSVView):
    queryset = Permission.objects.all()
    search_fields = {"name": "icontains"}


class NewPermission(SuccessMessageMixin, CreateView):
    template_name = "permissions/new.html"
    form_class = NewPermissionForm
    success_url = reverse_lazy("list-permissions")
    success_message = "Permission %(name)s was successfully created."


class DetailPermission(DetailView):
    template_name = "permissions/detail.html"
    queryset = Permission.objects.all()
    pk_url_kwarg = "permission_pk"


class UpdatePermission(SuccessMessageMixin, UpdateView):
    template_name = "permissions/update.html"
    form_class = UpdatePermissionForm
    queryset = Permission.objects.all()
    success_url = reverse_lazy("list-permissions")
    success_message = "Permission %(name)s was successfully updated."
    pk_url_kwarg = "permission_pk"


class DeletePermission(DeleteView):
    queryset = Permission.objects.all()
    template_name = "delete.html"
    success_url = reverse_lazy("list-permissions")
    pk_url_kwarg = "permission_pk"


class NewEmployeeRequest(SuccessMessageMixin, CreateView):
    template_name = "requests/new_employee_request.html"
    form_class = NewEmployeeRequestForm
    success_url = reverse_lazy("landing")
    success_message = "Employee Request submision was successful. You will be contacted soon."

    def form_valid(self, form):
        request = form.save()
        Log.objects.create(author="Anonymous", **request.creation_log())
        return super().form_valid(form)


class NewContractorRequest(SuccessMessageMixin, CreateView):
    template_name = "requests/new_contractor_request.html"
    form_class = NewContractorRequestForm
    success_url = reverse_lazy("landing")
    success_message = "Contractor Request submision was successful. You will be contacted soon."

    def form_valid(self, form):
        request = form.save()
        Log.objects.create(author="Anonymous", **request.creation_log())
        return super().form_valid(form)


class RequestsList(TemplateView):
    template_name = "requests/list.html"

    def get(self, request, *args, **kwargs):
        self.employee_requests = (
            EmployeeRequest.objects.all()
            .prefetch_related("permissions")
            .select_related("employee")
            .order_by("employee__first_name")
        )
        self.contractor_requests = (
            ContractorRequest.objects.all().prefetch_related("permissions").order_by("first_name")
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["employee_requests"] = self.employee_requests
        context["contractor_requests"] = self.contractor_requests
        return context


class DetailEmployeeRequest(DetailView):
    template_name = "requests/employee_detail.html"
    queryset = EmployeeRequest.objects.all()
    pk_url_kwarg = "request_pk"


class DetailContractorRequest(DetailView):
    template_name = "requests/contractor_detail.html"
    queryset = ContractorRequest.objects.all()
    pk_url_kwarg = "request_pk"


class RequestApprovalMixin:
    def process_approval(self, request):
        profile = self.request.user.amp_profile

        if profile.is_hr():
            request.hr_status = True
        elif profile.is_tc():
            request.tc_status = True
        elif profile.is_ace():
            request.ace_status = True
        elif profile.is_cip():
            request.cip_status = True

        request.save()
        return request

    def finalize_approval(self, request, change_log):
        Log.objects.create(author=self.request.user.email, **change_log)
        messages.success(
            self.request,
            "{resource_type} {resource_display}'s request was approved. Permissions have been transferred successfully.".format(
                resource_type=request.get_resource_type(),
                resource_display=request.get_resource_display(),
            ),
        )
        request.delete()


class ApproveEmployeeRequest(RequestApprovalMixin, View):
    def get(self, request, request_pk):
        employee_request = EmployeeRequest.objects.get(pk=request_pk)
        employee_request = self.process_approval(employee_request)

        if not employee_request.is_approved():
            return redirect("detail-employee-request", request_pk=employee_request.pk)

        employee = employee_request.employee
        old_permissions = employee.permissions.all()
        new_permissions = employee_request.permissions.all()
        employee.permissions.add(*new_permissions)

        change_log = employee.permission_change_log(old_permissions)
        self.finalize_approval(employee_request, change_log)
        return redirect("list-requests")


class ApproveContractorRequest(RequestApprovalMixin, View):
    def get(self, request, request_pk):
        contractor_request = ContractorRequest.objects.get(pk=request_pk)
        contractor_request = self.process_approval(contractor_request)

        if not contractor_request.is_approved():
            return redirect("detail-contractor-request", request_pk=contractor_request.pk)

        contractor, _ = Contractor.objects.get_or_create(
            first_name=contractor_request.first_name,
            last_name=contractor_request.last_name,
            email=contractor_request.email,
            employer=contractor_request.employer,
        )
        old_permissions = contractor.permissions.all()
        new_permissions = contractor_request.permissions.all()
        contractor.permissions.add(*new_permissions)
        change_log = contractor.permission_change_log(old_permissions)
        self.finalize_approval(contractor_request, change_log)
        return redirect("list-requests")


class RequestRejectionMixin:
    def process_rejection(self, request):
        profile = self.request.user.amp_profile

        if profile.is_hr():
            request.hr_status = False
        elif profile.is_tc():
            request.tc_status = False
        elif profile.is_ace():
            request.ace_status = False
        elif profile.is_cip():
            request.cip_status = False

        request.save()
        return request

    def finalize_rejection(self, request):
        Log.objects.create(
            category="Rejection",
            author=self.request.user.email,
            accessor=request.get_resource_type(),
            description="{resource_type} {resource_display}'s request for {permissions_list} rejected and deleted from the system.".format(
                resource_type=request.get_resource_type(),
                resource_display=request.get_resource_display(),
                permissions_list=", ".join(
                    request.permissions.all().values_list("name", flat=True)
                ),
            ),
        )
        messages.success(
            self.request,
            "{resource_type} {resource_display}'s request was rejected.".format(
                resource_type=request.get_resource_type(),
                resource_display=request.get_resource_display(),
            ),
        )
        request.delete()


class RejectEmployeeRequest(RequestRejectionMixin, View):
    def get(self, request, request_pk):
        employee_request = EmployeeRequest.objects.get(pk=request_pk)
        employee_request = self.process_rejection(employee_request)

        if not employee_request.is_rejected():
            return redirect("detail-employee-request", request_pk=employee_request.pk)

        self.finalize_rejection(employee_request)
        return redirect("list-requests")


class RejectContractorRequest(RequestRejectionMixin, View):
    def get(self, request, request_pk):
        contractor_request = ContractorRequest.objects.get(pk=request_pk)
        contractor_request = self.process_rejection(contractor_request)

        if not contractor_request.is_rejected():
            return redirect("detail-contractor-request", request_pk=contractor_request.pk)

        self.finalize_rejection(contractor_request)
        return redirect("list-requests")


class ListUsers(ListView):
    template_name = "users/list.html"
    queryset = get_user_model().objects.filter(amp_profile__isnull=False)


class NewUser(SuccessMessageMixin, CreateView):
    template_name = "users/new.html"
    form_class = NewUserForm
    success_url = reverse_lazy("list-users")
    success_message = "%(username)s was successfully created."


class UpdateUser(SuccessMessageMixin, UpdateView):
    template_name = "users/update.html"
    form_class = UpdateUserForm
    queryset = get_user_model().objects.all()
    success_url = reverse_lazy("list-users")
    success_message = "%(first_name)s %(last_name)s was successfully updated."
    pk_url_kwarg = "user_pk"


class DeleteUser(DeleteView):
    queryset = get_user_model().objects.all()
    template_name = "delete.html"
    success_url = reverse_lazy("list-users")
    pk_url_kwarg = "user_pk"
