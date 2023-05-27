import platform

bind = '0.0.0.0:8001'  # 绑定的IP地址和端口号
workers = 4  # 工作进程数量
backlog = 2048
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync模式，默认的是sync模式
worker_connections = 1000
timeout = 30
keepalive = 2
# debug = True
debug = True if platform.system() == 'Windows' else False
proc_name = 'gunicorn.pid'
pidfile = '/tmp/gunicorn.pid'
# logfile = '/tmp/debug.log'
logfile = '/tmp/gunicorn_debug.log'
loglevel = 'debug'
# accesslog = '/tmp/gunicorn_access.log'
accesslog = '/tmp/access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
daemon = True
