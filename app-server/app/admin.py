from django.contrib import admin

# Company Model
from app.models import Company

# Accessor Models
from app.models import Employee, EmployeeDocument, Contractor

# Permission Models
from app.models import Permission, Log

# Request Models
from app.models import EmployeeRequest, ContractorRequest

"""
                             COMPANY MODEL
"""


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['name']

"""
                             ACCESSOR MODELS
"""


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'first_name', 'last_name', 'company')
    search_fields = ['first_name', 'last_name']


class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['employee__first_name', 'employee__last_name']


class ContractorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'first_name', 'last_name', 'employer', 'company')
    search_fields = ['first_name', 'last_name']

"""
                             PERMISSION MODELS
"""


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'company')
    search_fields = ['name']


class LogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'author', 'accessor', 'category', 'company', 'creation_time')
    search_fields = ['author', 'accessor', 'accessor']

"""
                             REQUEST MODELS
"""


class EmployeeRequestAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'employee', 'company')
    search_fields = ['employee__first_name', 'employee__last_name']


class ContractorRequestAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'company', 'first_name', 'last_name', 'employer')
    search_fields = ['first_name', 'last_name']

# Register models to admin site

# Company Model
admin.site.register(Company, CompanyAdmin)

# Accessor Models
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeDocument, EmployeeDocumentAdmin)
admin.site.register(Contractor, ContractorAdmin)

# Permission Models
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Log, LogAdmin)

# Request Models
admin.site.register(EmployeeRequest, EmployeeRequestAdmin)
admin.site.register(ContractorRequest, ContractorRequestAdmin)
