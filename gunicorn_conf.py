
import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
errorlog = "-"
accesslog = "-"
loglevel = "info"
timeout = 120
forwarded_allow_ips = "*"
