from redis import Redis
from rq import Queue

redis_conn = Redis()  # By default localhost
queue = Queue(connection=redis_conn)
