FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /uber_lite

WORKDIR /uber_lite

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

COPY . /uber_lite/

RUN pip install -r requirements.txt