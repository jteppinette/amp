from django.contrib.auth import get_user_model
from django.db import models

CIP_MANAGER = "CIP Manager"
ALTERNATE_CIP_MANAGER = "Alternate CIP Manager"
ACCESS_CONTROL_ENGINEER = "Access Control Engineer"
TRAINING_COORDINATOR = "Training Coordinator"
HUMAN_RESOURCES = "Human Resources"
PROFILE_TITLES = (
    (CIP_MANAGER, CIP_MANAGER),
    (ALTERNATE_CIP_MANAGER, ALTERNATE_CIP_MANAGER),
    (ACCESS_CONTROL_ENGINEER, ACCESS_CONTROL_ENGINEER),
    (TRAINING_COORDINATOR, TRAINING_COORDINATOR),
    (HUMAN_RESOURCES, HUMAN_RESOURCES),
)

LOG_CATEGORIES = (
    ("Approval", "Approval"),
    ("Rejection", "Rejection"),
    ("New Employee", "New Employee"),
    ("New Contractor", "New Contractor"),
    ("Permission Change", "Permission Change"),
    ("New Employee Permission Request", "New Employee Permission Request"),
    ("New Contractor Permission Request", "New Contractor Permission Request"),
)


class Permission(models.Model):
    name = models.CharField(max_length=160)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), models.CASCADE, related_name="%(app_label)s_profile"
    )
    title = models.CharField(max_length=80, choices=PROFILE_TITLES, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def is_cip(self):
        return self.title == CIP_MANAGER or self.title == ALTERNATE_CIP_MANAGER

    def is_ace(self):
        return self.title == ACCESS_CONTROL_ENGINEER

    def is_tc(self):
        return self.title == TRAINING_COORDINATOR

    def is_hr(self):
        return self.title == HUMAN_RESOURCES


class Resource(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    permissions = models.ManyToManyField(Permission, related_name="%(class)ss")

    background_check = models.FileField(
        upload_to="background", blank=True, null=True, help_text="This field is not required."
    )
    last_background_check_date = models.DateField(
        blank=True, null=True, help_text="This field is not required. Ex. 2012-05-13"
    )
    last_training_date = models.DateField(
        blank=True, null=True, help_text="This is field is not required. Ex. 2012-05-13"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "{first_name} {last_name}".format(
            last_name=self.last_name, first_name=self.first_name
        )

    def permission_change_log(self, old_permissions):
        new_permissions = [permission.name for permission in self.permissions.all()]
        old_permissions = [permission.name for permission in old_permissions]

        old_permissions_msg = ", ".join(old_permissions) if old_permissions else "No Permissions"
        new_permissions_msg = ", ".join(new_permissions) if new_permissions else "No Permissions"

        return {
            "category": "Permission Change",
            "accessor": str(self),
            "description": (
                "{resource}'s permissions have been changed "
                "from [{old_permission_msg}] to [{new_permission_msg}]."
            ).format(
                resource=str(self),
                old_permission_msg=old_permissions_msg,
                new_permission_msg=new_permissions_msg,
            ),
        }

    def creation_log(self):
        if self.permissions.exists():
            description = "{resource} added to the system with permissions: {permissions}.".format(
                resource=str(self),
                permissions=", ".join([str(permission) for permission in self.permissions.all()]),
            )
        else:
            description = "{resource} added to the system without permissions.".format(
                resource=str(self)
            )

        category = "New {resource_type}".format(
            resource_type=self.__class__._meta.verbose_name.title()
        )
        return {"category": category, "accessor": str(self), "description": description}


class Employee(Resource):
    def __str__(self):
        return "Employee {resource}".format(resource=str(super()))


class EmployeeDocument(models.Model):
    file = models.FileField(upload_to="employee-documents")
    employee = models.ForeignKey(
        Employee,
        models.CASCADE,
        help_text="Which employee does this file reference?",
        related_name="documents",
    )

    def __str__(self):
        return "{file} - {employee}".format(file=self.file, employee=str(self.employee))


class Contractor(Resource):
    employer = models.CharField(max_length=80)

    def __str__(self):
        return "Contractor {resource}".format(resource=str(super()))


class ContractorDocument(models.Model):
    file = models.FileField(upload_to="contractor-documents")
    contractor = models.ForeignKey(
        Contractor,
        models.CASCADE,
        help_text="Which contractor does this file reference?",
        related_name="documents",
    )

    def __str__(self):
        return "{file} - {contractor}".format(file=self.file, contractor=str(self.contractor))


class Log(models.Model):
    ACCESSORS = (("Employee", "Employee"), ("Contractor", "Contractor"))

    category = models.CharField(max_length=160, choices=LOG_CATEGORIES)

    author = models.CharField(max_length=160)

    accessor = models.CharField(max_length=160)

    description = models.TextField()
    creation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Log: {msg}".format(
            msg=(self.description[:32] + "...") if len(self.description) > 35 else self.description
        )


class Request(models.Model):
    permissions = models.ManyToManyField(Permission, related_name="%(class)s_requests")

    hr_status = models.NullBooleanField(blank=True, null=True)
    tc_status = models.NullBooleanField(blank=True, null=True)
    ace_status = models.NullBooleanField(blank=True, null=True)
    cip_status = models.NullBooleanField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{permissions_count} permissions to {resource_display}".format(
            permissions_count=self.permissions.count(), resource_display=self.get_resource_display()
        )

    def is_approved(self):
        return self.hr_status and self.tc_status and self.ace_status and self.cip_status

    def is_rejected(self):
        return (
            self.hr_status is False
            and self.tc_status is False
            and self.ace_status is False
            and self.cip_status is False
        )

    def creation_log(self):
        resource_display = self.get_resource_display()
        resource_type = self.get_resource_type()
        return {
            "category": "New {resource_type} Permission Request".format(
                resource_type=resource_type
            ),
            "accessor": resource_display,
            "description": "{resource_display} requesting the following permissions: {permissions}.".format(
                resource_display=resource_display,
                permissions=", ".join(self.permissions.values_list("name", flat=True)),
            ),
        }


class EmployeeRequest(Request):
    employee = models.ForeignKey(Employee, models.CASCADE)

    def get_resource_display(self):
        return self.employee.get_full_name()

    def get_resource_type(self):
        return self.employee.__class__._meta.verbose_name.title()


class ContractorRequest(Request):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    employer = models.CharField(max_length=80)

    remote = models.BooleanField(help_text="Will you be accessing remotely?")

    background_check = models.FileField(upload_to="background", blank=True, null=True)

    def get_resource_display(self):
        return "{first_name} {last_name}".format(
            last_name=self.last_name, first_name=self.first_name
        )

    def get_resource_type(self):
        return "Contractor"
