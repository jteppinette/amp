"""
Detail the models that will be used in the AMP app.

The AMP models are seperated into the following groups:

    COMPANY MODEL:

        * Company

    NOTIFICATION MODEL:
        
        * Notification

    ACCESSOR MODELS:

        * Employee
        * Contractor

    PERMISSION MODELS:
        
        * Permission
        * Log

    REQUEST MODELS:

        * Employee Request
        * Contractor Request
"""

from django.db import models
from django.conf import settings

"""
                             COMPANY MODEL
"""


class Company(models.Model):
    name = models.CharField(max_length=160, unique=True)

    log_reccurence = models.IntegerField(help_text='Represent the time between automatic log emails. This field is measured in days.', default=7)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return self.name

"""
                             ACCESSOR MODELS
"""


class Employee(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    company = models.ForeignKey(Company)
    eid = models.IntegerField(unique=True)

    permissions = models.ManyToManyField('Permission', blank=True, null=True)

    background_check = models.FileField(upload_to='background', blank=True, null=True, help_text='This field is not required.')
    last_background_check_date = models.DateField(blank=True, null=True, help_text='This field is not required. Ex. 2012-05-13')

    last_training_date = models.DateField(blank=True, null=True, help_text='This is field is not required. Ex. 2012-05-13')

    def __unicode__(self):
        return 'Employee %s, %s' % (self.last_name, self.first_name)

    def permission_change_log(self, old_permissions):
        """
        Generate the log for a change in this Employee's permissions.
        """
        log = {'category': 'Permission Change',
               'accessor': '%s, %s' % (self.last_name, self.first_name),
               'company': self.company}

        permissions = self.permissions.all()

        new_permissions_list = []

        for permission in permissions:
            new_permissions_list.append(str(permission.name))

        old_permissions_list = []

        for permission in old_permissions:
            old_permissions_list.append(str(permission.name))

        old_permissions_msg = None
        new_permissions_msg = None

        if old_permissions_list:
            old_permissions_msg = ', '.join(old_permissions_list)
        else:
            old_permissions_msg = 'No Permissions'

        if new_permissions_list:
            new_permissions_msg = ', '.join(new_permissions_list)
        else:
            new_permissions_msg = 'No Permissions'

        log['description'] = "Employee %s %s's permissions have been changed from [%s] to [%s]." % (self.first_name, self.last_name, old_permissions_msg, new_permissions_msg)

        return log

    def creation_log(self):
        log = {'category': 'New Employee',
               'accessor': '%s, %s' % (self.last_name, self.first_name),
               'company': self.company}

        permissions = self.permissions.all()
        permission_list = []

        for permission in permissions:
            permission_list.append(str(permission.name))

        if permission_list:
            log['description'] = 'Employee %s, %s added to the system with permissions %s.' % (self.last_name, self.first_name, ', '.join(permission_list))
        else:
            log['description'] = 'Employee %s, %s added to the system without permissions.' % (self.last_name, self.first_name)

        return log


    class Meta:
        unique_together = (('first_name', 'last_name', 'company'), ('company', 'eid'))


class EmployeeDocument(models.Model):
    file = models.FileField(upload_to='employee-documents', blank=True, null=True, help_text='This field is not required.')
    employee = models.ForeignKey(Employee, help_text='This field represent the employee that this document belongs to.', related_name='documents')

    def __unicode__(self):
        return 'Document %s of %s' % (self.employee, self.file)


class Contractor(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()

    employer = models.CharField(max_length=80)
    company = models.ForeignKey(Company, help_text="This field represents the company that the contractor is requesting access to.")

    permissions = models.ManyToManyField('Permission', blank=True, null=True)

    background_check = models.FileField(upload_to='background', blank=True, null=True, help_text='This field is not required.')
    last_background_check_date = models.DateField(blank=True, null=True, help_text='This field is not required. Ex. 2012-05-13')

    last_training_date = models.DateField(blank=True, null=True, help_text='This field is not required. Ex. 2012-05-13')

    def __unicode__(self):
        return 'Contractor %s, %s' % (self.last_name, self.first_name)

    def permission_change_log(self, old_permissions):
        log = {'category': 'Permission Change',
               'accessor': '%s, %s' % (self.last_name, self.first_name),
               'company': self.company}

        permissions = self.permissions.all()

        new_permissions_list = []

        for permission in permissions:
            new_permissions_list.append(str(permission.name))

        old_permissions_list = []

        for permission in old_permissions:
            old_permissions_list.append(str(permission.name))

        old_permissions_msg = None
        new_permissions_msg = None

        if old_permissions_list:
            old_permissions_msg = ', '.join(old_permissions_list)
        else:
            old_permissions_msg = 'No Permissions'

        if new_permissions_list:
            new_permissions_msg = ', '.join(new_permissions_list)
        else:
            new_permissions_msg = 'No Permissions'

        log['description'] = "Contractor %s %s's permissions have been changed from [%s] to [%s]." % (self.first_name, self.last_name, old_permissions_msg, new_permissions_msg)

        return log


    def creation_log(self):
        log = {'category': 'New Contractor',
               'accessor': '%s, %s' % (self.last_name, self.first_name),
               'company': self.company}

        permissions = self.permissions.all()
        permission_list = []

        for permission in permissions:
            permission_list.append(str(permission.name))

        if permission_list:
            log['description'] = 'Contractor %s, %s from %s has been added to the system with permissions %s.' % (self.last_name, self.first_name, self.employer, ', '.join(permission_list))
        else:
            log['description'] = 'Contractor %s, %s from %s has been added to the system without permissions.' % (self.last_name, self.first_name, self.employer)

        return log


    class Meta:
        unique_together = ('first_name', 'last_name', 'company')

"""
                             PERMISSION MODELS
"""


class Permission(models.Model):
    name = models.CharField(max_length=160)

    company = models.ForeignKey(Company)

    def __unicode__(self):
        return '%s created by %s' % (self.name, str(self.company))


class Log(models.Model):
    CATEGORIES = (
        ('Approval', 'Approval'),
        ('Rejection', 'Rejection'),
        ('New Employee', 'New Employee'),
        ('New Contractor', 'New Contractor'),
        ('Permission Change', 'Permission Change'),
        ('New Employee Permission Request', 'New Employee Permission Request'),
        ('New Contractor Permission Request', 'New Contractor Permission Request')
    )

    ACCESSORS = (
        ('Employee', 'Employee'),
        ('Contractor', 'Contractor')
    )

    company = models.ForeignKey(Company)

    category = models.CharField(max_length=160, choices=CATEGORIES)

    author = models.CharField(max_length=160)

    accessor = models.CharField(max_length=160)

    description = models.TextField()
    creation_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        description = self.description
        if len(description) >= 35:
            description = description[:32]
            elipse = '...'
            message = description + elipse
        else:
            message = description

        return 'Log: %s' % (message)

"""
                             REQUEST MODELS
"""


class EmployeeRequest(models.Model):
    company = models.ForeignKey(Company)
    employee = models.ForeignKey(Employee)
    permissions = models.ManyToManyField(Permission)

    hr_status = models.NullBooleanField(blank=True, null=True)
    tc_status = models.NullBooleanField(blank=True, null=True)
    ace_status = models.NullBooleanField(blank=True, null=True)
    cip_status = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return 'Employee request by %s' % (str(self.employee))

    def creation_log(self):
        log = {'category': 'New Employee Permission Request',
               'accessor': '%s, %s' % (self.employee.last_name, self.employee.first_name),
               'company': self.company}

        permissions = self.permissions.all()
        permission_list = []

        for permission in permissions:
            permission_list.append(str(permission.name))

        log['description'] = 'New employee request for %s, %s requesting the following permissions: %s.' % (self.employee.last_name, self.employee.first_name, ', '.join(permission_list))

        return log


class ContractorRequest(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    employer = models.CharField(max_length=80)

    company = models.ForeignKey(Company)

    permissions = models.ManyToManyField(Permission)

    remote = models.BooleanField(help_text="Will you be accessing remotely?")

    background_check = models.FileField(upload_to='background', blank=True, null=True)

    hr_status = models.NullBooleanField(blank=True, null=True)
    tc_status = models.NullBooleanField(blank=True, null=True)
    ace_status = models.NullBooleanField(blank=True, null=True)
    cip_status = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return 'Contractor request by Contractor %s, %s' % (self.last_name, self.first_name)

    def creation_log(self):
        log = {'category': 'New Contractor Permission Request',
               'accessor': '%s, %s' % (self.last_name, self.first_name),
               'company': self.company}

        permissions = self.permissions.all()
        permission_list = []

        for permission in permissions:
            permission_list.append(str(permission.name))

        log['description'] = 'New contractor request for %s, %s requesting the following permissions: %s.' % (self.last_name, self.first_name, ', '.join(permission_list))

        return log


# Import Receivers
from app import receivers
