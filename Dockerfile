FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/code
WORKDIR /opt/code

COPY requirements.txt .
RUN pip install --default-timeout=1000 -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD gunicorn -w 2 -b 0.0.0.0:8000 --chdir /opt/code wsgi:application --reload --timeout 900