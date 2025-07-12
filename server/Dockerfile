# syntax=docker/dockerfile:1
FROM python:3.12.3
WORKDIR /raspberry_server
RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get install libgpiod2
RUN pip install opencv-python
RUN pip install adafruit-circuitpython-dht

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD [ "python3", "/raspberry_server/start_server.py" ]
