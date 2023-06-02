#!/usr/bin/env bash


flask db init
flask db migrate -m "Initial migration"
flask db upgrade

gunicorn app:app -w $WORKERS --worker-class=gevent --bind $API_HOST:$API_PORT
exec "$@"