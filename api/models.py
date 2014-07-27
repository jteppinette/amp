"""
Detail the models that will be used in the AMP api.

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
    """
    Represents a company that can use the amp software.
    """
    name = models.CharField(max_length=160, unique=True)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return self.name

"""
                             NOTIFICATION MODEL
"""


class Notification(models.Model):
    """
    Represents a notification that will be sent to a user.
    """
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return "%s | %s" % (self.title, self.description)

"""
                             ACCESSOR MODELS
"""


class Employee(models.Model):
    """ Represents an employee at a specific amp company. This model is used to
    request and track permissions between individuals.
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    company = models.ForeignKey(Company)
    eid = models.IntegerField()

    permissions = models.ManyToManyField('Permission', blank=True, null=True)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return 'Employee %s, %s' % (self.last_name, self.first_name)

    class Meta:
        unique_together = (('first_name', 'last_name', 'company'), ('company', 'eid'))


class Contractor(models.Model):
    """
    Represents a contractor for a specific amp company. This model is used to
    request and track permissions between contractors.
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()

    employer = models.CharField(max_length=80)
    company = models.ForeignKey(Company, help_text="This field represents the company that the contractor is requesting access to.")

    permissions = models.ManyToManyField('Permission', blank=True, null=True)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return 'Contractor %s, %s' % (self.last_name, self.first_name)

    class Meta:
        unique_together = ('first_name', 'last_name', 'company')

"""
                             PERMISSION MODELS
"""


class Permission(models.Model):
    """
    Represents a permission that has given to an `Accessor`.
    """
    name = models.CharField(max_length=160)

    company = models.ForeignKey(Company)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return '%s created by %s' % (self.name, str(self.company))


class Log(models.Model):
    """
    Represents a change log of permissions.
    """
    ACCESSORS = (
        ('Employee', 'Employee'),
        ('Contractor', 'Contractor')
    )

    author = models.CharField(max_length=160)

    accessor_type = models.CharField(max_length=160, choices=ACCESSORS)
    accessor = models.CharField(max_length=160)

    change = models.TextField()
    creation_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return 'Change to %s %s by %s' % (self.accessor_type, self.accessor, self.author)

"""
                             REQUEST MODELS
"""


class EmployeeRequest(models.Model):
    """
    Represents a request made to gain permissions by an employee.
    """
    employee = models.ForeignKey(Employee)
    permissions = models.ManyToManyField(Permission)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return 'Employee request by %s' % (str(self.employee))


class ContractorRequest(models.Model):
    """
    Represents a request made to gain permissions by a contractor.
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    employer = models.CharField(max_length=80)

    permissions = models.ManyToManyField(Permission)

    remote = models.BooleanField()

    background_check = models.FileField(upload_to='background', blank=True, null=True)

    def __unicode__(self):
        """
        Provide a unicode representation of this model.
        """
        return 'Contractor request by Contractor %s, %s' % (self.last_name, self.first_name)
