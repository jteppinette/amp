FROM tiangolo/uwsgi-nginx

ENV DEBUG False

COPY nginx.conf /etc/nginx/conf.d/

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN touch data.sqlite3

CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py createfixturedata -f && /usr/bin/supervisord
