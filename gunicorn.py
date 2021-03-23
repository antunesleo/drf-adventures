import os

errorlog = "-"
max_requests = int(os.getenv("WEB_MAX_REQUESTS", 500))
max_requests_jitter = int(os.getenv("WEB_MAX_REQUESTS_JITTER", 150))
workers = int(os.getenv("WEB_CONCURRENCY", 3))
worker_class = "gevent"
