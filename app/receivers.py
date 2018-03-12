from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from app.models import EmployeeRequest, ContractorRequest


@receiver(post_save, sender=EmployeeRequest)
def employee_request_notification(sender, **kwargs):
    if kwargs['created'] is False:
        return

    inst = kwargs['instance']

    users = get_user_model().objects.filter(company=inst.company)
    to_list = []
    for user in users:
        to_list.append(user.email)

    msg = {
        'subject': 'Notification: New Employee Request',
        'content': 'A new employee request has been created by %s %s.' % (inst.employee.first_name, inst.employee.last_name),
        'from': settings.EMAIL_FROM,
        'to': to_list
    }

    send_mail(msg['subject'], msg['content'], msg['from'], msg['to'], fail_silently=False)

@receiver(post_save, sender=ContractorRequest)
def contractor_request_notification(sender, **kwargs):
    if kwargs['created'] is False:
        return

    inst = kwargs['instance']

    users = get_user_model().objects.filter(company=inst.company)
    to_list = []
    for user in users:
        to_list.append(user.email)

    msg = {
        'subject': 'Notification: New Contractor Request',
        'content': 'A new contractor request has been created by %s %s.' % (inst.first_name, inst.last_name),
        'from': settings.EMAIL_FROM,
        'to': to_list
    }

    send_mail(msg['subject'], msg['content'], msg['from'], msg['to'], fail_silently=False)
