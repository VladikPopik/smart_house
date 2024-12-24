# syntax=docker/dockerfile:1
FROM python:3.12.3
WORKDIR /motion
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8881
COPY . .
CMD [ "python3", "/motion/start_server.py" ]