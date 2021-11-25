import multiprocessing

wsgi_app="wsgi:app"
bind = "0.0.0.0:8080"
timeout = 600
workers = multiprocessing.cpu_count()*2+1
loglevel = "debug"
keepalive = 40
worker_class = "gevent"
daemon = True