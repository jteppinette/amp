# AMP - *a permissions and employee/contractor management system*

======

## Initialize Environment

1. Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

2. `git clone https://github.com/jteppinette/amp.git`

3. `vagrant up` - _Initialize and provison the Ubuntu Trust 64 virtual machine._

4. `vagrant ssh` - _Create an ssh tunnel using port 2222 on the localhost ip._

5. `cd /vagrant/app-server`

6. `source venv/bin/activate`- _Activate the Python2.7 virtual environment. This virtual environment contains all necessary Python packages. These packages are described in the requirements file located at /vagrant/app-server/requirements.txt._

7. `python manage.py createsuperuser` - _Create a user by following the Django *createsuperuser* command prompts. This superuser will be used to create companies and administor the AMP system._

8. Visit `http://localhost:8080/admin` and login with your superuser credentials.

9. Create a new Company by visiting the  *Company* page listed in the *App* panel of the administrator site.

10. Create a new CIP Manager for this Company by visiting the  *Users* page listed in the *Authentication* panel of the administrator site.

11. Visit `http://localhost:8080/` and login as the CIP Manager that you have just created. - _This is the account that can be used to fully manage this individual company._

## Development

After the steps listed above in the _Initialize Environment_ section have been completed, then you can begin to develop the application.
Developing or maintaining this application is as simple as editing the many views, template, models and etc.. files listed under the app-server directory.
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
