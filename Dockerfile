FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./config.yaml /code/config.yaml

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
