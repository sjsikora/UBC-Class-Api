# syntax=docker/dockerfile:1

FROM python:3.9-buster

EXPOSE 5000/tcp

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./main.py"]