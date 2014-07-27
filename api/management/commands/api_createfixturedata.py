from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import urllib2
import json

# Custom User Model
from django.contrib.auth import get_user_model

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


class Command(BaseCommand):
    """
    Create a large set of fixture data for  visual testing.
    """

    def handle(self, *args, **kwargs):
        """
        Prompt the user, asking if he/she would truly like to delete all
        objects.
        """
        print 'Are you sure you would like to recreate your entire database?'
        print 'Enter `DELETE` to delete database and load with fixture data: '
        choice = raw_input()
        if choice != 'DELETE':
            print 'Your actions have resulted in zero change to the database.'
            return

        """
        Generate Companies.
        """
        # Delete pre-existing objects
        Company.objects.all().delete()

        lus = Company.objects.create(name='LUS')

        """
        Generate Users.
        """
        # Delete pre-existing objects
        get_user_model().objects.all().exclude(is_admin=True).delete()

        users = [
            {'first_name': 'Sean', 'last_name': 'Johnson', 'email': 'sean.johnson@lus.com'},
            {'first_name': 'Tyler', 'last_name': 'Coody', 'email': 'tyler.coody@lus.com'},
            {'first_name': 'John', 'last_name': 'Easton', 'email': 'john.easton@lus.com'},
            {'first_name': 'Dustin', 'last_name': 'Howard', 'email': 'dustin.howard@lus.com'},
            {'first_name': 'Will', 'last_name': 'Todd', 'email': 'will.todd@lus.com'},
        ]

        # Create new users
        for idx, title in enumerate(get_user_model().TITLES):
            print get_user_model().objects.create_user(email=users[idx]['email'], password='lus', first_name=users[idx]['first_name'], last_name=users[idx]['last_name'], title=title[0], company=lus)
