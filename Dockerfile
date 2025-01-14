FROM python:3.12-slim-bullseye

COPY requirements.txt /temp/requirements.txt
COPY Django_project /Django_project

WORKDIR /Django_project

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password dogs-user

USER dogs-user