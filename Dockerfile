
FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir pika

COPY . .

ENV PYTHONUNBUFFERED=1