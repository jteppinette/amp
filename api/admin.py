"""
Define the model admin page.
"""

from django.contrib import admin

# Company Model
from api.models import Company

# Notification Model
from api.models import Notification

# Accessor Models
from api.models import Employee, Contractor

# Permission Models
from api.models import Permission, Log

# Request Models
from api.models import EmployeeRequest, ContractorRequest

"""
                             COMPANY MODEL
"""


class CompanyAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `Company` model.
    """
    list_display = ('__unicode__',)
    search_fields = ['name']

"""
                             NOTIFICATION MODEL
"""


class NotificationAdmin(admin.ModelAdmin):
    """
    Define the custom charactersitics for the `Notification` model.
    """
    list_display = ('title', 'description', 'user')

"""
                             ACCESSOR MODELS
"""


class EmployeeAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `Employee` model.
    """
    list_display = ('__unicode__', 'first_name', 'last_name', 'company')
    search_fields = ['first_name', 'last_name']


class ContractorAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `Contractor` model.
    """
    list_display = ('__unicode__', 'first_name', 'last_name', 'employer', 'company')
    search_fields = ['first_name', 'last_name']

"""
                             PERMISSION MODELS
"""


class PermissionAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `Permission` model.
    """
    list_display = ('__unicode__', 'name', 'company')
    search_fields = ['name']


class LogAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `Log` model.
    """
    list_display = ('__unicode__', 'author', 'accessor', 'category', 'company', 'creation_time')
    search_fields = ['author', 'accessor', 'accessor']

"""
                             REQUEST MODELS
"""


class EmployeeRequestAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `EmployeeRequest` model.
    """
    list_display = ('__unicode__', 'employee', 'company')
    search_fields = ['employee__first_name', 'employee__last_name']


class ContractorRequestAdmin(admin.ModelAdmin):
    """
    Define the custom characteristics for the `ContractorRequest` model.
    """
    list_display = ('__unicode__', 'company', 'first_name', 'last_name', 'employer')
    search_fields = ['first_name', 'last_name']

# Register models to admin site

# Company Model
admin.site.register(Company, CompanyAdmin)

# Notification Model
admin.site.register(Notification, NotificationAdmin)

# Accessor Models
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Contractor, ContractorAdmin)

# Permission Models
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Log, LogAdmin)

# Request Models
admin.site.register(EmployeeRequest, EmployeeRequestAdmin)
admin.site.register(ContractorRequest, ContractorRequestAdmin)
