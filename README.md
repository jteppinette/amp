# AMP - *a permissions and employee/contractor management system*

## Development

### Required Software

* [docker](https://docs.docker.com/)
* [git](https://git-scm.com/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

### Getting Started

```
$ git clone https://github.com/jteppinette/amp.git && cd amp`
$ virtualenv venv`
$ source venv/bin/activate`
$ pip install -r requirements.txt`
$ docker-compose up -d db minio mail`
$ python manage.py makemigrations`
$ python manage.py migrate`
$ python manage.py createfixturedata`
$ python manage.py runserver`
```

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
* DB_PORT         `default: 5432`
* MINIO_ACCESSKEY `default: access-key`
* MINIO_BUCKET    `default: test`
* MINIO_SERVER    `default: 0.0.0.0:9000`
* MINIO_SECURE    `default: false`
* MINIO_SECRET    `default: 'secret-key, insecure: true`
* SESSION_SECRET  `defualt: secret, insecure: true`
* MAIL_FROM       `default: notifications@test-company.localhost')
* MAIL_HOST       `default: 0.0.0.0`
* MAIL_PORT       `default: 1025`
* MAIL_PASSWORD   `default: `
* MAIL_USER       `default: `
* MAIL_USE_TLS    `default: False`
* MAIL_USE_SSL    `default: False`

### Company Settings

For personalization and routing, the *APP_URL*, *MAIL_FROM*, and *COMPANY_NAME* configuration items should be set.

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
