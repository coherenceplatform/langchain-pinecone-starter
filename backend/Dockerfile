FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . /app/