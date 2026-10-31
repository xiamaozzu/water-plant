"""
gunicorn 配置（Linux 生产环境）
启动命令: gunicorn -c gunicorn_config.py app.web:app
"""
import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60
keepalive = 5

# 日志
accesslog = "/var/log/water-plant/access.log"
errorlog = "/var/log/water-plant/error.log"
loglevel = "info"

# 进程名
proc_name = "water-plant"
