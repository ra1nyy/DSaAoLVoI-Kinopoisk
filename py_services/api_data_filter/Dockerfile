FROM python:3.11

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --deploy --system

COPY . .

EXPOSE 8080