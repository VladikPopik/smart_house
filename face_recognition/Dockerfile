# syntax=docker/dockerfile:1
FROM python:3.12.10
WORKDIR /face_recognition
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8889
COPY . .
CMD [ "python3", "/face_recognition/main.py" ]