# AMP - *a permissions and employee/contractor management system*

## Development

### Required Software

* [docker](https://docs.docker.com/)
* [git](https://git-scm.com/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

### Getting Started

1. `git clone https://github.com/jteppinette/risk-managed.git`

2. `virtualenv venv`

3. `source venv/bin/activate`

4. `pip install -r requirements.txt`

5. `docker-compose up -d db`

6. `python manage.py migrate`

7. `python manage.py createfixturedata`

8. `python manage.py runserver`

## Usage

### Environment Variables

Any variables marked as `insecure: true` should be overriden before being added to a production system.

* APP_URL         `default: http://localhost:8000/`
* COMPANY_NAME    `default: Test Company`
* DEBUG           `default: True`
* DB_NAME         `default: db`
* DB_USER         `default: db`
* DB_PASSWORD     `defualt: secret, insecure: true`
* DB_HOST         `default: 0.0.0.0`
* DB_PORT         `default: 3306`
* SESSION_SECRET  `defualt: secret, insecure: true`

### Docker

1. `docker build . -t app`

2. `docker run \
      -d
      -e MYSQL_DATABASE=db
      -e MYSQL_USER=db
      -e MYSQL_PASSWORD=db-secret
      -e MYSQL_RANDOM_ROOT_PASSWORD=yes
      --name db
      mysql`

3. `docker run
      -d
      -p 8000:80
      -e SESSION_SECRET=session-secret
      -e DB_NAME=db
      -e DB_USER=db
      -e DB_PORT=3306
      -e DB_PASSWORD=db-secret
      -e DB_HOST=db
      --link db
      --name app
      app`

4. `docker exec -it app python manage.py migrate`

5. `docker exec -it app python manage.py createsuperuser`

### Email

An important group of setting to be aware of are the ones based around email.
By default, the [_'django.core.mail.backends.filebased.EmailBackend'_](https://docs.djangoproject.com/en/1.8/topics/email/#file-backend) is used.
In a production environment, this backend should be replaced by the [_'django.core.mail.backends.smpt.EmailBackend'_](https://docs.djangoproject.com/en/1.8/topics/email/#smtp-backend).
Read the linked documentation for information on setting this up.

### Company Settings

For personalization and routing, the *APP_URL* and *COMPANY_NAME* configuration items should be set after initializing your envionrment, setting up DNS routing, and creating an initial company.

## Features

The AMP system offers many different features and capabilities that are defined and reachable through the dashboard.

### Structure

Each key feature of AMP is broken down into either a list page with individual detail or a single detail page.

* List Pages:
    * List pages offer the ability to _Create_, _Edit_, _Delete_, _Search_, and _Export_ the data they represent. If you click on the edit, _pencil_ icon, you will be redirected the the individual detail page.
* Detail Pages:
    * Detail pages offer the ability to modify a single object.

### Notifications

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
