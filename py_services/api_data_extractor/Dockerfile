FROM python:3.11

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --system

EXPOSE 8080