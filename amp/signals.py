from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from amp.models import ContractorRequest, EmployeeRequest


@receiver(post_save, sender=ContractorRequest)
@receiver(post_save, sender=EmployeeRequest)
def employee_request_notification(sender, created, instance, *args, **kwargs):
    if not created:
        return

    resource_type = instance.get_resource_type()
    resource_display = instance.get_resource_display()
    send_mail(
        subject="{prefix}New {resource_type} Request".format(
            prefix=settings.EMAIL_SUBJECT_PREFIX, resource_type=resource_type
        ),
        message="A new {resource_type} request has been created by {resource_display}.".format(
            resource_type=resource_type, resource_display=resource_display
        ),
        from_email=settings.DEFAULT_EMAIL_FROM,
        recipient_list=[user.email for user in get_user_model().objects.all()],
    )
