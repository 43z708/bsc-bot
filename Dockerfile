FROM python:3.8-alpine as python-base
# We need gcc and libc-dev
RUN apk update && \
    apk add --no-cache gcc libc-dev && \
    mkdir -p /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install --upgrade pip  && \
    pip install -r requirements.txt  && \
    chmod -R 766 ./
