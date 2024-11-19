FROM python:3.13-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./config.yaml /code/config.yaml

VOLUME /data

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

CMD ["python", "app/main.py"]
