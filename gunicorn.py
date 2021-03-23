import os

errorlog = "-"
max_requests = int(os.getenv("WEB_MAX_REQUESTS", 500))
workers = int(os.getenv("WEB_CONCURRENCY", 3))
worker_class = "gevent"
