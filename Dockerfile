FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY ./config.yaml /app/config.yaml

VOLUME /data

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app

CMD ["python", "main.py"]
