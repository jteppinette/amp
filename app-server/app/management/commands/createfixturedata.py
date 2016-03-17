from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import urllib2
import json
import random

# Custom User Model
from django.contrib.auth import get_user_model

# Company Model
from app.models import Company

# Accessor Models
from app.models import Employee, Contractor

# Permission Models
from app.models import Permission, Log

# Request Models
from app.models import EmployeeRequest, ContractorRequest


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
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

        company = Company.objects.create(name=settings.COMPANY_NAME)
	company_email = company.name.replace(' ', '').lower()
        print company

        """
        Generate Users.
        """
        # Delete pre-existing objects
        get_user_model().objects.all().exclude(is_admin=True).delete()

        users = [
            {'first_name': 'Sean', 'last_name': 'Johnson', 'email': 'sean.johnson@' + company_email + '.com'},
            {'first_name': 'Tyler', 'last_name': 'Coody', 'email': 'tyler.coody@' + company_email + '.com'},
            {'first_name': 'John', 'last_name': 'Easton', 'email': 'john.easton@' + company_email + '.com'},
            {'first_name': 'Dustin', 'last_name': 'Howard', 'email': 'dustin.howard@' + company_email + '.com'},
            {'first_name': 'Will', 'last_name': 'Todd', 'email': 'will.todd@' + company_email + '.com'},
        ]

        # Create new users
        for idx, title in enumerate(get_user_model().TITLES):
            print get_user_model().objects.create_user(email=users[idx]['email'], password=users[idx]['first_name'].lower(), first_name=users[idx]['first_name'], last_name=users[idx]['last_name'], title=title[0], company=company)

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
            print Permission.objects.create(name=name, company=company)

        """
        Generate Employees.
        """
        # Delete pre-existing objects
        Employee.objects.all().delete()

        # Get employee information
        response = urllib2.urlopen('http://www.json-generator.com/api/json/get/bSIuhdYYZe?indent=2') 
        employee_info_list = json.loads(response.read())

        for info in employee_info_list:
            employee = Employee.objects.create(company=company, **info)
            print employee
            
            Log.objects.create(author='Fixture Data Script', **employee.creation_log())

        # Add permissions to random Employees
        employee_list = Employee.objects.all()
        permissions_list = Permission.objects.all()

        for i in range(10):
            employee = random.choice(employee_list)
            permission = random.choice(permissions_list)

            old_permissions = employee.permissions.all()
            length = len(old_permissions)
            employee.permissions.add(permission.id)
            
            employee.save()

            Log.objects.create(author='Fixture Data Script', **employee.permission_change_log(old_permissions))

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

            contractor = Contractor.objects.create(company=company, employer=employer, email=email.replace(' ', '').lower(), **info)
            print contractor

            Log.objects.create(author='Fixture Data Script', **contractor.creation_log())

        # Add permissions to random Contractors
        contractor_list = Contractor.objects.all()
        permissions_list = Permission.objects.all()

        for i in range(10):
            contractor = random.choice(contractor_list)
            permission = random.choice(permissions_list)

            old_permissions = contractor.permissions.all()
            length = len(old_permissions)
            contractor.permissions.add(permission.id)
            
            contractor.save()

            Log.objects.create(author='Fixture Data Script', **contractor.permission_change_log(old_permissions))
        
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
                    request = EmployeeRequest.objects.create(employee=employee, company=company)
                    request.permissions.add(permission.id)
                    request.save()
                    print request

                    Log.objects.create(author='Fixture Data Script', **request.creation_log())

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
                                                               remote=random.choice([True, False]),
                                                               company=company)
                    request.permissions.add(permission.id)
                    request.save()
                    print request

                    Log.objects.create(author='Fixture Data Script', **request.creation_log())

                    break
