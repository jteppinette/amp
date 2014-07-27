from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import urllib2
import json
import random

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
        print lus

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

        """
        Generate Employees.
        """
        # Delete pre-existing objects
        Employee.objects.all().delete()

        # Get employee information
        response = urllib2.urlopen('http://www.json-generator.com/api/json/get/bSIuhdYYZe?indent=2') 
        employee_info_list = json.loads(response.read())

        for info in employee_info_list:
            print Employee.objects.create(company=lus, **info)


        """
        Generate Contractors.
        """
        # Delete pre-existing objects
        Contractor.objects.all().delete()

        # Contractor Companies
        companies = ['Engineering United', 'American Electric', 'Southern Engineering', 'Microsoft Computers']

        # Get contractor information
        response = urllib2.urlopen('http://www.json-generator.com/api/json/get/bWOaYaiesy?indent=2') 
        contractor_info_list = json.loads(response.read())

        for info in contractor_info_list:
            employer = random.choice(companies)
            email = '%s.%s@%s.com' % (info['first_name'], info['last_name'], employer)

            print Contractor.objects.create(company=lus, employer=employer, email=email.replace(' ', '').lower(), **info)

        """
        Generate Permissions.
        """
        # Delete pre-existing objects
        Permission.objects.all().delete()

        permission_names = [
            'Admin EMS Access',
            'Read-Only PACS Access',
            'Regular User Firewall Accounts Access',
            'Physical PCC Access',
        ]

        for name in permission_names:
            print Permission.objects.create(name=name, company=lus)

        """
        Generate EmployeeRequests.
        """
        # Delete pre-existing objects
        EmployeeRequest.objects.all().delete()
        
        employee_list = Employee.objects.all()
        permission_list = Permission.objects.all()

        for i in range(10):
            while True:
                employee = random.choice(employee_list)
                permission = random.choice(permission_list)

                if permission in employee.permissions.all():
                    print 'Failure to maintain unique integrity.'
                    continue
                else:
                    request = EmployeeRequest.objects.create(employee=employee)
                    request.permissions.add(permission.id)
                    request.save()
                    print request
                    break

        """
        Generate ContractorRequests.
        """
        # Delete pre-existing objects
        ContractorRequest.objects.all().delete()
        
        contractor_list = Contractor.objects.all()
        permission_list = Permission.objects.all()

        for i in range(10):
            while True:
                contractor = random.choice(contractor_list)
                permission = random.choice(permission_list)

                if permission in contractor.permissions.all():
                    print 'Failure to maintain unique integrity.'
                    continue
                else:
                    request = ContractorRequest.objects.create(first_name=contractor.first_name,
                                                               last_name=contractor.last_name,
                                                               employer=contractor.employer,
                                                               email=contractor.email,
                                                               remote=random.choice([True, False]))
                    request.permissions.add(permission.id)
                    request.save()
                    print request
                    break
