#!/usr/bin/env bash


alembic upgrade head

gunicorn app:app -w $WORKERS --worker-class=gevent --bind $API_HOST:$API_PORT
exec "$@"