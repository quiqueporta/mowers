FROM python:3.7-alpine

WORKDIR /mowers

ENV PYTHONPATH="/mowers/src"

COPY ./requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY . /mowers
