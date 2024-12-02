# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /motion
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8881
COPY . .
CMD [ "python3", "/motion/start_server.py" ]