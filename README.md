# AMP - *a permissions and employee/contractor management system*

## Initialize Environment

Upon receiving the AMP system for development or production uses, the following information will allow you to get your environment setup and ready for use.

1. Install `pip` and `virtualenv`

2. `git clone https://github.com/jteppinette/amp.git`

3. `virtualenv amp`

5. `source amp/bin/activate`

9. `python manage.py createsuperuser` - _Create a user by following the Django *createsuperuser* command prompts. This superuser will be used to create companies and administor the AMP system._

10. Visit `http://localhost:8000/admin` and login with your superuser credentials.

11. Create a new Company by visiting the  *Company* page listed in the *App* panel of the administrator site.

12. Create a new CIP Manager for this Company by visiting the  *Users* page listed in the *Authentication* panel of the administrator site.

13. Visit `http://localhost:8000/` and login as the CIP Manager that you have just created. - _This is the account that can be used to fully manage this individual company._

### Fixture Data

Fixture data can be loaded into the AMP system by executing the following commands after provisioning the environment with Ansible:

1. `source venv/bin/activate`- _Activate the Python2.7 virtual environment. This virtual environment contains all necessary Python packages. These packages are described in the requirements file located at /vagrant/app-server/requirements.txt._

2. `python manage.py createfixturedata`

3. You can now login to the system at `http://localhost:8080/auth/login/` with the credentials of email: `sean.johson@testcompany.com` and password: `sean`.

## Settings

There are many settings and features that are configurable in the _/<root>/project/settings.py_ file.
Some of which are also made available through environment variables.
Read through this file for detailed documentation regarding each available setting, or
view the online [Django v1.8 Documentation](https://docs.djangoproject.com/en/1.8/ref/settings/).

## Docker

1. `docker build . -t amp`

2. `docker run -it -e SECRET_KEY=<secret> -e APP_URL=<url> -e COMPANY_NAME=<company_name> -P --rm --name amp amp`

### Email

An important group of setting to be aware of are the ones based around email.
By default, the [_'django.core.mail.backends.filebased.EmailBackend'_](https://docs.djangoproject.com/en/1.8/topics/email/#file-backend) is used.
In a production environment, this backend should be replaced by the [_'django.core.mail.backends.smpt.EmailBackend'_](https://docs.djangoproject.com/en/1.8/topics/email/#smtp-backend).
Read the linked documentation for information on setting this up.

### Company Settings

For personalization and routing, the *APP_URL* and *COMPANY_NAME* configuration items should be set after initializing your envionrment, setting up DNS routing, and creating an initial company.

### Debug

In a producton environment, be sure to set the *DEBUG* configuration item to _False_. This will disable the automatic wen interface error reporting and expensive debugging routines.

## Features

The AMP system offers many different features and capabilities that are defined and reachable through the dashboard.

### Structure

Each key feature of AMP is broken down into either a list page with individual detail or a single detail page.

* List Pages:
    * List pages offer the ability to _Create_, _Edit_, _Delete_, _Search_, and _Export_ the data they represent. If you click on the edit, _pencil_ icon, you will be redirected the the individual detail page.
* Detail Pages:
    * Detail pages offer the ability to modify a single object.

## Notifications

The AMP system sends many alerts and notifications that react to user input and regular time schedules.

* Employee Request Notification: 
    * Employee request notifications are sent upon an employee registering into the system. This registration occurs on the unauthenticated landing page found under the _Make Employee Request_ heading.
    * This notification is sent to all users of the requested Company.

* Contractor Request Notification: 
    * Contractor request notifications are sent upon a contractor registering into the system. This registration occurs on the unauthenticated landing page found under the _Make Contractor Request_ heading.
    * This notification is sent to all users of the requested Company.

* Recurring Log Notification:
    * The entire log count will be sent via email to all company users at an interval set through the _Log Reccurence_ input on the _Settings_ page.
    * By default, these logs will be mailed out once per day.
