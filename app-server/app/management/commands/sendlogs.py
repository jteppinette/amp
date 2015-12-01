from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.core.mail import send_mail

from django.contrib.auth import get_user_model

from django.conf import settings

from djqscsv import write_csv, generate_filename

from app.models import Log, Company

import os
import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        queryset = Log.objects.all().order_by('-creation_time')
        filename = generate_filename(queryset, append_datestamp=True)

        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'logs')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'logs'))

        with open(os.path.join(settings.MEDIA_ROOT, 'logs', filename), 'w') as f:
            log_file = File(f)
            write_csv(queryset.values(), log_file)

        company = Company.objects.get(name=settings.COMPANY_NAME)

        if datetime.datetime.today().day % company.log_reccurence == 0:
            users = get_user_model().objects.filter(company=company)
            to_list = []
            for user in users:
                to_list.append(user.email)

            msg = {
                'subject': 'Log Report',
                'content': 'Log Report Download: %s%slogs/%s' % (settings.APP_URL, settings.MEDIA_URL, filename),
                'from': 'notifications@gdsamp.com',
                'to': to_list
            }

            send_mail(msg['subject'], msg['content'], msg['from'], msg['to'], fail_silently=False)
