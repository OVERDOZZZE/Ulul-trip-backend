FROM python:3.10

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /home/app/

RUN pip install -r requirements.txt

COPY . /home/app/

#CMD ['python', 'manage.py runserver 0.0.0.0:8000']


