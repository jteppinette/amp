FROM python:2.7-onbuild

EXPOSE 8080

RUN touch data.sqlite3

CMD python manage.py migrate && python manage.py createfixturedata -f && python manage.py runserver 0.0.0.0:8080 --insecure
