from django.contrib import admin

from amp.models import (
    Contractor,
    ContractorDocument,
    ContractorRequest,
    Employee,
    EmployeeDocument,
    EmployeeRequest,
    Log,
    Permission,
    Profile,
)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "first_name", "last_name")
    search_fields = ["first_name", "last_name"]


class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ["employee__first_name", "employee__last_name"]


class ContractorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "first_name", "last_name", "employer")
    search_fields = ["first_name", "last_name"]


class ContractorDocumentAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ["contractor__first_name", "contractor__last_name"]


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name")
    search_fields = ["name"]


class LogAdmin(admin.ModelAdmin):
    list_display = ("__str__", "author", "accessor", "category", "creation_time")
    search_fields = ["author", "accessor", "accessor"]


class EmployeeRequestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "employee")
    search_fields = ["employee__first_name", "employee__last_name"]


class ContractorRequestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "first_name", "last_name", "employer")
    search_fields = ["first_name", "last_name"]


admin.site.register(Profile)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeDocument, EmployeeDocumentAdmin)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(ContractorDocument, ContractorDocumentAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(EmployeeRequest, EmployeeRequestAdmin)
admin.site.register(ContractorRequest, ContractorRequestAdmin)
