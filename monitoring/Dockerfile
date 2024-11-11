# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /monitoring
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 9999
COPY . .
CMD [ "python3", "/monitoring/start_server.py" ]