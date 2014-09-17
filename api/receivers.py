"""
Define receivers for AMP application.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api.models import EmployeeRequest, ContractorRequest

from django.contrib.auth import get_user_model

import smtplib

@receiver(post_save, sender=EmployeeRequest)
def employee_request_notification(sender, **kwargs):
    """
    Send an email notifiatin to all officers about new Employee Request.
    """
    if kwargs['created'] is False:
        return

    inst = kwargs['instance']

    users = get_user_model().objects.filter(company=inst.company)
    to_list = []
    for user in users:
        to_list.append(user.email)

    # Mandrill Code
    msg = MIMEMultipart('alternative')

    msg['Subject'] = 'Notification: New Employee Request'
    msg['From'] = 'notifications@gdsamp.com'
    msg['To'] = ', '.join(to_list)

    text = 'A new employee request has been created by %s %s.' % (inst.employee.first_name, inst.employee.last_name)
    part1 = MIMEText(text, 'plain')

    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    msg.attach(part1)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)

    s.login(username, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())

    s.quit()

@receiver(post_save, sender=ContractorRequest)
def contractor_request_notification(sender, **kwargs):
    """
    Send an email notifiatin to all officers about new Contractor Request.
    """
    if kwargs['created'] is False:
        return

    inst = kwargs['instance']

    users = get_user_model().objects.filter(company=inst.company)
    to_list = []
    for user in users:
        to_list.append(user.email)

    # Mandrill Code
    msg = MIMEMultipart('alternative')

    msg['Subject'] = 'Notification: New Contractor Request'
    msg['From'] = 'notifications@gdsamp.com'
    msg['To'] = ', '.join(to_list)

    text = 'A new contractor request has been created by %s %s.' % (inst.first_name, inst.last_name)
    part1 = MIMEText(text, 'plain')

    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    msg.attach(part1)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)

    s.login(username, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())

    s.quit()
