FROM python:3.11-slim-buster

WORKDIR /opt/app
ENV PYTHONPATH=/opt/app/src

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT gunicorn manage:app -w $WORKERS --worker-class=gevent --bind $API_HOST:$API_PORT