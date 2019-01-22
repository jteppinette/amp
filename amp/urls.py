from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path

from amp import views

urlpatterns += [
    path("", views.Landing.as_view(), name="landing"),
    path("dashboard", views.Dashboard.as_view(), name="dashboard"),
    path("requests/employee/new/", views.NewEmployeeRequest.as_view(), name="new-employee-request"),
    path(
        "requests/contractor/new/",
        views.NewContractorRequest.as_view(),
        name="new-contractor-request",
    ),
    path(
        "dashboard/account/general/update",
        views.AccountGeneralUpdate.as_view(),
        name="account-general-update",
    ),
    path(
        "dashboard/account/password/change",
        views.AccountPasswordChange.as_view(),
        name="account-password-change",
    ),
    path("dashboard/users/", views.ListUsers.as_view(), name="list-users"),
    path("dashboard/users/new/", views.NewUser.as_view(), name="new-user"),
    path("dashboard/users/<int:user_pk>/update/", views.UpdateUser.as_view(), name="update-user"),
    path("dashboard/users/<int:user_pk>/delete/", views.DeleteUser.as_view(), name="delete-user"),
    path("dashboard/logs/", views.ListLogs.as_view(), name="list-logs"),
    path("dashboard/logs/csv", views.CSVLogs.as_view(), name="csv-logs"),
    path("dashboard/employees/", views.ListEmployees.as_view(), name="list-employees"),
    path("dashboard/employees/csv", views.CSVEmployees.as_view(), name="csv-employees"),
    path("dashboard/employees/new/", views.NewEmployee.as_view(), name="new-employee"),
    path(
        "dashboard/employees/<int:employee_pk>/update/",
        views.UpdateEmployee.as_view(),
        name="update-employee",
    ),
    path(
        "dashboard/employees/<int:employee_pk>/delete/",
        views.DeleteEmployee.as_view(),
        name="delete-employee",
    ),
    path(
        "dashboard/employees/<int:employee_pk>/documents/new/",
        views.NewEmployeeDocument.as_view(),
        name="new-employee-document",
    ),
    path(
        "dashboard/employees/<int:employee_pk>/documents/<int:document_pk>/delete/",
        views.DeleteEmployeeDocument.as_view(),
        name="delete-employee-document",
    ),
    path("dashboard/contractors/", views.ListContractors.as_view(), name="list-contractors"),
    path("dashboard/contractors/csv", views.CSVContractors.as_view(), name="csv-contractors"),
    path("dashboard/contractors/new/", views.NewContractor.as_view(), name="new-contractor"),
    path(
        "dashboard/contractors/<int:contractor_pk>/update/",
        views.UpdateContractor.as_view(),
        name="update-contractor",
    ),
    path(
        "dashboard/contractors/<int:contractor_pk>/delete/",
        views.DeleteContractor.as_view(),
        name="delete-contractor",
    ),
    path(
        "dashboard/contractors/<int:contractor_pk>/documents/new/",
        views.NewContractorDocument.as_view(),
        name="new-contractor-document",
    ),
    path(
        "dashboard/contractors/<int:contractor_pk>/documents/<int:document_pk>/delete/",
        views.DeleteContractorDocument.as_view(),
        name="delete-contractor-document",
    ),
    path("dashboard/permissions/", views.ListPermissions.as_view(), name="list-permissions"),
    path("dashboard/permissions/csv", views.CSVPermissions.as_view(), name="csv-permissions"),
    path("dashboard/permissions/new/", views.NewPermission.as_view(), name="new-permission"),
    path(
        "dashboard/permissions/<int:permission_pk>",
        views.DetailPermission.as_view(),
        name="detail-permission",
    ),
    path(
        "dashboard/permissions/<int:permission_pk>/update/",
        views.UpdatePermission.as_view(),
        name="update-permission",
    ),
    path(
        "dashboard/permissions/<int:permission_pk>/delete/",
        views.DeletePermission.as_view(),
        name="delete-permission",
    ),
    path("dashboard/requests/", views.RequestsList.as_view(), name="list-requests"),
    path(
        "dashboard/requests/employees/<int:request_pk>/approve/",
        views.ApproveEmployeeRequest.as_view(),
        name="approve-employee-request",
    ),
    path(
        "dashboard/requests/employees/<int:request_pk>/reject/",
        views.RejectEmployeeRequest.as_view(),
        name="reject-employee-request",
    ),
    path(
        "dashboard/requests/employees/<int:request_pk>/",
        views.DetailEmployeeRequest.as_view(),
        name="detail-employee-request",
    ),
    path(
        "dashboard/requests/contractors/<int:request_pk>/approve/",
        views.ApproveContractorRequest.as_view(),
        name="approve-contractor-request",
    ),
    path(
        "dashboard/requests/contractors/<int:request_pk>/reject/",
        views.RejectContractorRequest.as_view(),
        name="reject-contractor-request",
    ),
    path(
        "dashboard/requests/contractors/<int:request_pk>/",
        views.DetailContractorRequest.as_view(),
        name="detail-contractor-request",
    ),
    path("admin/", admin.site.urls),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
