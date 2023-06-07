sleep 5
sh -c python3 /tests/functional/utils/wait_for_redis.py \
&& pytest /tests/functional/src