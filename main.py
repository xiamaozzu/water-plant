"""
水厂主体软件 - 主入口
同时启动：
  1) 控制台常驻任务（后台线程，周期打印 Hello World）
  2) Flask Web 服务（主线程，http://127.0.0.1:5000）
"""
import threading
import time
import sys

from app.config import WEB_HOST, WEB_PORT
from app.console import console_loop
from app.web import app
from app import db


def main():
    # 初始化数据库（建库 + 建表）
    print("[Main] 正在初始化数据库 ...", flush=True)
    try:
        db.init_database()
        print("[Main] 数据库初始化完成。", flush=True)
    except Exception as e:
        print(f"[Main][ERROR] 数据库初始化失败：{e}", flush=True)
        print("[Main] 请确认 MySQL 服务已启动且 root/root 可连接。", flush=True)
        sys.exit(1)

    # 启动控制台后台线程
    stop_event = threading.Event()
    t = threading.Thread(target=console_loop, args=(stop_event,), daemon=True)
    t.start()

    # 启动 Flask（主线程）
    print(f"[Main] Web 服务启动：http://{WEB_HOST}:{WEB_PORT}", flush=True)
    try:
        app.run(host=WEB_HOST, port=WEB_PORT, debug=False, use_reloader=False)
    finally:
        stop_event.set()
        t.join(timeout=3)


if __name__ == "__main__":
    main()
