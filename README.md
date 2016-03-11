# AMP - *a permissions and employee/contractor management system*

## Initialize Environment

Upon receiving the AMP system for development or production uses, the following information will allow you to get your environment setup and ready for use.

1. Install [Vagrant](https://www.vagrantup.com/downloads.html), and [VirtualBox](https://www.virtualbox.org/wiki/Downloads), and [Ansible](https://www.ansible.com).

2. `git clone https://github.com/jteppinette/amp.git`

3. `vagrant up` - _Initialize the Ubuntu Trust 64 virtual machine._

5. `ansible-playbook provision/development.provisioner.yml -i localhost.inventory.ini -u vagrant -k`

6. `vagrant ssh` - _Create an ssh tunnel using port 2222 on the localhost ip._

7. `cd /vagrant/app-server`

8. `source venv/bin/activate`- _Activate the Python2.7 virtual environment. This virtual environment contains all necessary Python packages. These packages are described in the requirements file located at /vagrant/app-server/requirements.txt._

9. `python manage.py createsuperuser` - _Create a user by following the Django *createsuperuser* command prompts. This superuser will be used to create companies and administor the AMP system._

10. Visit `http://localhost:8080/admin` and login with your superuser credentials.

11. Create a new Company by visiting the  *Company* page listed in the *App* panel of the administrator site.

12. Create a new CIP Manager for this Company by visiting the  *Users* page listed in the *Authentication* panel of the administrator site.

13. Visit `http://localhost:8080/` and login as the CIP Manager that you have just created. - _This is the account that can be used to fully manage this individual company._

## Development

After the steps listed above in the _Initialize Environment_ section have been completed, then you can begin to develop the application.
Developing or maintaining this application is as simple as editing the many views, templates, models, and utility files listed under the app-server directory.
After you have made a change, it is necessary to run `sudo service apache2 restart` to restart the Django server.
This restart will force a reloading of the necessary Python assets and will make your new changes available on the next page refresh.

## Settings

There are many settings and features that are configurable in the _/vagrant/app-server/project/settings.py_ file.
Read through this file for detailed documentation regarding each available setting, or
view the online [Django v1.8 Documentation](https://docs.djangoproject.com/en/1.8/ref/settings/).

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

The AMP system offers many different features and capablities that are defined and reachable through the dashboard.

### Struture

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

## Backup

The AMP system does not come configured with backup systems for the database or media assets (logs, backgound checks, files, etc..). These systems are left to the individual system administrator to be implemented.

* [PostgreSQL Backup](http://www.postgresql.org/docs/9.1/static/backup.html): This set of documentation will provide information on exporting and importing PostgreSQL raw data.
* Media Backup: Media files are stored in a diretory determined by the *MEDIA_ROOT* setting in *settings.py*. Typically, an [rsync](http://linux.die.net/man/1/rsync) command would be setup throug a [chronjob](http://man7.org/linux/man-pages/man5/crontab.5.html), so that the directory can be backed up on a remote system at a regular interval.

