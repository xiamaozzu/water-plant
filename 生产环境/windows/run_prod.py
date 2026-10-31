"""
生产环境启动入口（Windows）
使用 waitress 作为 WSGI 服务器（替代 gunicorn，Windows 兼容）
"""
import os
import sys

# 将项目根目录加入 sys.path（本文件在 生产环境/windows/ 下，需向上两级）
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _project_root)
os.chdir(_project_root)

from waitress import serve
from app.web import app
from app import db
import threading
from app.console import console_loop

if __name__ == "__main__":
    # 初始化数据库
    print("[生产] 正在初始化数据库 ...", flush=True)
    try:
        db.init_database()
        print("[生产] 数据库初始化完成。", flush=True)
    except Exception as e:
        print(f"[生产][ERROR] 数据库初始化失败：{e}", flush=True)
        sys.exit(1)

    # 启动控制台后台线程
    stop_event = threading.Event()
    t = threading.Thread(target=console_loop, args=(stop_event,), daemon=True)
    t.start()

    # 用 waitress 启动 Web 服务，监听 127.0.0.1:5000（Nginx 反向代理到此）
    print("[生产] Web 服务启动：http://127.0.0.1:5000 (waitress)", flush=True)
    serve(app, host="127.0.0.1", port=5000, threads=8)
