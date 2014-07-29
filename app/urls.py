"""
Define the routing used to find the AMP pages.
"""

from django.conf.urls import patterns, url, include

from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = patterns('',
    # Authentication
    url(r'^login/$', views.auth_login, name="auth_login"),
    url(r'^logout/$', views.auth_logout, name="auth_login"),
    
    # General
    url(r'^$', views.home, name="home"),

    # App
    url(r'^dashboard/$', login_required(views.dashboard), name="dashboard"),

    # New Requests
    url(r'^requests/employee/new/$', views.NewEmployeeRequest.as_view(), name='new_employee_request'),
    url(r'^requests/contractor/new/$', views.NewContractorRequest.as_view(), name='new_contractor_request'),

    # Account
    url(r'^dashboard/account/$', login_required(views.UpdateAccount.as_view()), name='update_account'),

    # Company
    url(r'^dashboard/company/$', login_required(views.company), name='company'),
    url(r'^dashboard/company/user/new/$', login_required(views.NewCompanyUser.as_view()), name='new_company_user'),

    # Logs
    url(r'^dashboard/logs/$', login_required(views.ListLogs.as_view()), name='logs'),

    # Employees
    url(r'^dashboard/employees/$', login_required(views.ListEmployees.as_view()), name='employees'),
    url(r'^dashboard/employees/(?P<pk>\d+)/$', login_required(views.UpdateEmployee.as_view()), name='update_employee'),

    # Contractors
    url(r'^dashboard/contractors/$', login_required(views.ListContractors.as_view()), name='contractors'),
    url(r'^dashboard/contractors/(?P<pk>\d+)/$', login_required(views.UpdateContractor.as_view()), name='update_contractor'),

    # Permissions
    url(r'^dashboard/permissions/$', login_required(views.ListPermissions.as_view()), name='permissions'),
    url(r'^dashboard/permissions/(?P<pk>\d+)/$', login_required(views.UpdatePermission.as_view()), name='update_permission'),
    url(r'^dashboard/permissions/new/$', login_required(views.NewPermission.as_view()), name='new_permission'),

)
