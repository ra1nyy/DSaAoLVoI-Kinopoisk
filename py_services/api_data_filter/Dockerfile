FROM python:3.11

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --system

RUN apt-get update
RUN apt-get install -y default-jre

EXPOSE 8080