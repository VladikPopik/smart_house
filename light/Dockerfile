# syntax=docker/dockerfile:1
FROM python:3.12.3
WORKDIR /light
RUN apt-get update 
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --use-pep517
EXPOSE 9999
COPY . .
CMD [ "python3", "/light/start_server.py" ]