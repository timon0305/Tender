FROM python:2.7-alpine3.6

RUN apk update && apk add \
        postgresql-dev \
        python-dev \
        gcc \
        jpeg-dev \
        zlib-dev \
        musl-dev \
        linux-headers && \
        mkdir app

WORKDIR /app/

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

ADD . /app/

RUN if [ -s requirements.txt ]; then pip install -r requirements.txt; fi
EXPOSE 8092
VOLUME /app/auction/assets
ENTRYPOINT ["/usr/local/bin/uwsgi", "--ini", "/app/uwsgi.ini"]

