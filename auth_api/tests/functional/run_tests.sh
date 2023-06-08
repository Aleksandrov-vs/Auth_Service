#!/usr/bin/env sh

sleep 10
sh -c python3 /tests/functional/utils/wait_for_redis.py \
&& pytest /tests/functional/src