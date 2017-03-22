from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = [
    # General
    url('^$', views.home, name='discover-home'),

    # App
    url('^dashboard/$', login_required(views.dashboard), name="dashboard-home"),

    # New Requests
    url('^requests/employee/new/$', views.NewEmployeeRequest.as_view(), name='new-employee-request'),
    url('^requests/contractor/new/$', views.NewContractorRequest.as_view(), name='new-contractor-request'),

    # Account
    url('^dashboard/account/$', login_required(views.UpdateAccount.as_view()), name='update-account'),

    # Account
    url('^dashboard/settings/$', login_required(views.UpdateSettings.as_view()), name='update-settings'),

    # Users
    url('^dashboard/users/$', login_required(views.ListUsers.as_view()), name='list-users'),
    url('^dashboard/users/new/$', login_required(views.NewUser.as_view()), name='new-user'),
    url('^dashboard/users/(?P<pk>\d+)/update/$', login_required(views.UpdateUser.as_view()), name='update-user'),
    url('^dashboard/users/(?P<pk>\d+)/delete/$', login_required(views.DeleteUser.as_view()), name='delete-user'),

    # Logs
    url('^dashboard/logs/$', login_required(views.ListLogs.as_view()), name='list-logs'),
    url('^dashboard/logs/csv$', login_required(views.CSVLogs.as_view()), name='csv-logs'),

    # Employees
    url('^dashboard/employees/$', login_required(views.ListEmployees.as_view()), name='list-employees'),
    url('^dashboard/employees/csv$', login_required(views.CSVEmployees.as_view()), name='csv-employees'),
    url('^dashboard/employees/new/$', login_required(views.NewEmployee.as_view()), name='new-employee'),
    url('^dashboard/employees/(?P<pk>\d+)/update/$', login_required(views.UpdateEmployee.as_view()), name='update-employee'),
    url('^dashboard/employees/(?P<pk>\d+)/delete/$', login_required(views.DeleteEmployee.as_view()), name='delete-employee'),

    # Employee Documents
    url('^dashboard/employees/(?P<employee>\d+)/documents/new/$', login_required(views.NewEmployeeDocument.as_view()), name='new-employee-document'),
    url('^dashboard/employees/(?P<employee>\d+)/documents/(?P<pk>\d+)/delete/$', login_required(views.DeleteEmployeeDocument.as_view()), name='delete-employee-document'),

    # Contractors
    url('^dashboard/contractors/$', login_required(views.ListContractors.as_view()), name='list-contractors'),
    url('^dashboard/contractors/csv$', login_required(views.CSVContractors.as_view()), name='csv-contractors'),
    url('^dashboard/contractors/new/$', login_required(views.NewContractor.as_view()), name='new-contractor'),
    url('^dashboard/contractors/(?P<pk>\d+)/update/$', login_required(views.UpdateContractor.as_view()), name='update-contractor'),
    url('^dashboard/contractors/(?P<pk>\d+)/delete/$', login_required(views.DeleteContractor.as_view()), name='delete-contractor'),

    # Contractor Documents
    url(r'^dashboard/contractors/(?P<contractor>\d+)/documents/new/$', login_required(views.NewContractorDocument.as_view()), name='new-contractor-document'),
    url(r'^dashboard/contractors/(?P<contractor>\d+)/documents/(?P<pk>\d+)/delete/$', login_required(views.DeleteContractorDocument.as_view()), name='delete-contractor-document'),

    # Permissions
    url('^dashboard/permissions/$', login_required(views.ListPermissions.as_view()), name='list-permissions'),
    url('^dashboard/permissions/csv$', login_required(views.CSVPermissions.as_view()), name='csv-permissions'),
    url('^dashboard/permissions/new/$', login_required(views.NewPermission.as_view()), name='new-permission'),
    url('^dashboard/permissions/(?P<pk>\d+)/$', login_required(views.DetailPermission.as_view()), name='detail-permission'),
    url('^dashboard/permissions/(?P<pk>\d+)/update/$', login_required(views.UpdatePermission.as_view()), name='update-permission'),
    url('^dashboard/permissions/(?P<pk>\d+)/delete/$', login_required(views.DeletePermission.as_view()), name='delete-permission'),

    # Requests
    url('^dashboard/requests/$', login_required(views.requests), name='list-requests'),
    url('^dashboard/requests/employees/(?P<pk>\d+)/approve/$', login_required(views.approve_employee_request), name='approve-employee-request'),
    url('^dashboard/requests/employees/(?P<pk>\d+)/reject/$', login_required(views.reject_employee_request), name='reject-employee-request'),
    url('^dashboard/requests/employees/(?P<pk>\d+)/$', login_required(views.DetailEmployeeRequest.as_view()), name='detail-employee-request'),
    url('^dashboard/requests/contractors/(?P<pk>\d+)/approve/$', login_required(views.approve_contractor_request), name='approve-contractor-request'),
    url('^dashboard/requests/contractors/(?P<pk>\d+)/reject/$', login_required(views.reject_contractor_request), name='reject-contractor-request'),
    url('^dashboard/requests/contractors/(?P<pk>\d+)/$', login_required(views.DetailContractorRequest.as_view()), name='detail-contractor-request'),

    # Admin
    url('^admin/', admin.site.urls),
]
