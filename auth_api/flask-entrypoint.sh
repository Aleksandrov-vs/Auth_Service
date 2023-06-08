#!/usr/bin/env bash

sleep 7

alembic upgrade head

gunicorn app:app -w $WORKERS --worker-class=gevent --bind $API_HOST:$API_PORT
exec "$@"