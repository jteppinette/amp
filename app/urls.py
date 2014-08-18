"""
Define the routing used to find the AMP pages.
"""

from django.conf.urls import patterns, url, include

from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = patterns('',
    # General
    url(r'^$', views.home, name='discover-home'),

    # App
    url(r'^dashboard/$', login_required(views.dashboard), name="dashboard-home"),

    # New Requests
    url(r'^requests/employee/new/$', views.NewEmployeeRequest.as_view(), name='new-employee-request'),
    url(r'^requests/contractor/new/$', views.NewContractorRequest.as_view(), name='new-contractor-request'),

    # Account
    url(r'^dashboard/account/$', login_required(views.UpdateAccount.as_view()), name='update-account'),

    # Company
    url(r'^dashboard/company/users/$', login_required(views.ListCompanyUsers.as_view()), name='list-company-users'),
    url(r'^dashboard/company/users/new/$', login_required(views.NewCompanyUser.as_view()), name='new-company-user'),
    url(r'^dashboard/company/users/(?P<pk>\d+)/update/$', login_required(views.UpdateCompanyUser.as_view()), name='update-company-user'),
    url(r'^dashboard/company/users/(?P<pk>\d+)/delete/$', login_required(views.DeleteCompanyUser.as_view()), name='delete-company-user'),

    # Logs
    url(r'^dashboard/logs/$', login_required(views.ListLogs.as_view()), name='list-logs'),

    # Employees
    url(r'^dashboard/employees/$', login_required(views.ListEmployees.as_view()), name='list-employees'),
    url(r'^dashboard/employees/new/$', login_required(views.NewEmployee.as_view()), name='new-employee'),
    url(r'^dashboard/employees/(?P<pk>\d+)/update/$', login_required(views.UpdateEmployee.as_view()), name='update-employee'),
    url(r'^dashboard/employees/(?P<pk>\d+)/delete/$', login_required(views.DeleteEmployee.as_view()), name='delete-employee'),

    # Contractors
    url(r'^dashboard/contractors/$', login_required(views.ListContractors.as_view()), name='list-contractors'),
    url(r'^dashboard/contractors/new/$', login_required(views.NewContractor.as_view()), name='new-contractor'),
    url(r'^dashboard/contractors/(?P<pk>\d+)/update/$', login_required(views.UpdateContractor.as_view()), name='update-contractor'),
    url(r'^dashboard/contractors/(?P<pk>\d+)/delete/$', login_required(views.DeleteContractor.as_view()), name='delete-contractor'),

    # Permissions
    url(r'^dashboard/permissions/$', login_required(views.ListPermissions.as_view()), name='list-permissions'),
    url(r'^dashboard/permissions/new/$', login_required(views.NewPermission.as_view()), name='new-permission'),
    url(r'^dashboard/permissions/(?P<pk>\d+)/$', login_required(views.DetailPermission.as_view()), name='detail-permission'),
    url(r'^dashboard/permissions/(?P<pk>\d+)/update/$', login_required(views.UpdatePermission.as_view()), name='update-permission'),
    url(r'^dashboard/permissions/(?P<pk>\d+)/delete/$', login_required(views.DeletePermission.as_view()), name='delete-permission'),

    # Requests
    url(r'^dashboard/requests/$', login_required(views.requests), name='list-requests'),
    url(r'^dashboard/requests/employees/(?P<pk>\d+)/approve/$', login_required(views.approve_employee_request), name='approve-employee-request'),
)
