import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from amp.models import PROFILE_TITLES, Contractor, Employee, Permission, Profile

USERS = [
    {"first_name": "Sean", "last_name": "Johnson", "username": "sean.johnson"},
    {"first_name": "Tyler", "last_name": "Coody", "username": "tyler.coody"},
    {"first_name": "John", "last_name": "Easton", "username": "john.easton"},
    {"first_name": "Dustin", "last_name": "Howard", "username": "dustin.howard"},
    {"first_name": "Will", "last_name": "Todd", "username": "will.todd"},
]

PERMISSIONS = [
    "Admin EMS Access",
    "Read-Only PACS Access",
    "Regular User Firewall Accounts Access",
    "Physical PCC Access",
]

EMPLOYEES = [
    {"first_name": "Barker", "last_name": "Frye"},
    {"first_name": "Villarreal", "last_name": "Bond"},
    {"first_name": "Prince", "last_name": "Spears"},
    {"first_name": "Orr", "last_name": "Blackwell"},
    {"first_name": "Mitchell", "last_name": "Garza"},
    {"first_name": "Rose", "last_name": "Sweeney"},
    {"first_name": "Brock", "last_name": "Santos"},
    {"first_name": "Glenda", "last_name": "Reese"},
    {"first_name": "Leona", "last_name": "Burton"},
    {"first_name": "Angela", "last_name": "Knight"},
    {"first_name": "Cooke", "last_name": "Cruz"},
    {"first_name": "Cheryl", "last_name": "Mcintyre"},
    {"first_name": "Merrill", "last_name": "Hooper"},
    {"first_name": "Hopkins", "last_name": "Lloyd"},
    {"first_name": "Manning", "last_name": "Contreras"},
    {"first_name": "Josie", "last_name": "Mcdonald"},
    {"first_name": "Maryann", "last_name": "Morse"},
    {"first_name": "Preston", "last_name": "Hunter"},
    {"first_name": "Joyce", "last_name": "Larsen"},
    {"first_name": "Lakisha", "last_name": "Graham"},
    {"first_name": "Graves", "last_name": "Melton"},
    {"first_name": "Cain", "last_name": "Kemp"},
    {"first_name": "Frieda", "last_name": "Arnold"},
    {"first_name": "Madeline", "last_name": "Pena"},
    {"first_name": "Matthews", "last_name": "Clark"},
    {"first_name": "Gwen", "last_name": "Weaver"},
    {"first_name": "Kimberly", "last_name": "Becker"},
    {"first_name": "Brewer", "last_name": "Cash"},
    {"first_name": "Lowery", "last_name": "Jennings"},
    {"first_name": "Laura", "last_name": "Leblanc"},
]

CONTRACTORS = [
    {"first_name": "Dudley", "last_name": "Frank"},
    {"first_name": "Elba", "last_name": "Hansen"},
    {"first_name": "Underwood", "last_name": "Acosta"},
    {"first_name": "Sweet", "last_name": "Francis"},
    {"first_name": "Clayton", "last_name": "Padilla"},
    {"first_name": "Spears", "last_name": "Sears"},
    {"first_name": "Burns", "last_name": "Mayer"},
    {"first_name": "Petra", "last_name": "Hendricks"},
    {"first_name": "Mavis", "last_name": "Reyes"},
    {"first_name": "Conner", "last_name": "Oneal"},
]

EMPLOYERS = [
    "Engineering United",
    "American Electric",
    "Southern Engineering",
    "Microsoft Computers",
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-f", "--force", action="store_true", dest="force", default=False, help="Force DB Wipe"
        )

    def handle(self, *args, **kwargs):
        if not kwargs.get("force"):
            print("Are you sure you would like to recreate your entire database?")
            print("Enter `DELETE` to delete database and load with fixture data: ")
            choice = input()
            if choice != "DELETE":
                print("Your actions have resulted in zero change to the database.")
                return

        company_domain = "{name}.com".format(name=settings.COMPANY_NAME.replace(" ", "").lower())

        random.seed(0)

        """
        Generate Users.
        """
        get_user_model().objects.all().exclude(is_superuser=True).delete()

        for idx, title in enumerate(PROFILE_TITLES):
            user = get_user_model().objects.create_user(
                email="{username}@{domain}".format(
                    username=USERS[idx]["username"], domain=company_domain
                ),
                password=USERS[idx]["first_name"].lower(),
                username=USERS[idx]["username"],
                first_name=USERS[idx]["first_name"],
                last_name=USERS[idx]["last_name"],
            )
            Profile.objects.create(user=user, title=title[0])

        """
        Generate Permissions.
        """
        Permission.objects.all().delete()

        [Permission.objects.create(name=permission) for permission in PERMISSIONS]

        """
        Generate Employees.
        """
        Employee.objects.all().delete()

        [Employee.objects.create(**employee) for employee in EMPLOYEES]

        """
        Generate Contractors.
        """
        Contractor.objects.all().delete()

        [
            Contractor.objects.create(employer=random.choice(EMPLOYERS), **contractor)
            for contractor in CONTRACTORS
        ]
