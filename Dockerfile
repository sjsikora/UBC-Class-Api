# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

EXPOSE 5000/tcp

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./main.py"]