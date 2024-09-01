# syntax=docker/dockerfile:1
FROM python:3.12
WORKDIR /smart_house
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8001
COPY . .
CMD [ "python3", "/smart_house/start_manager_server.py" ]