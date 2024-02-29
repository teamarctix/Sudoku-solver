FROM python:3.10.4-slim-buster
RUN apt update && apt upgrade -y
COPY requirements.txt .

RUN pip3 install --no-cache-dir -U -r requirements.txt
WORKDIR /app
COPY . .
CMD gunicorn --bind 0.0.0.0:$PORT app:app
