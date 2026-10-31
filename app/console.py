"""控制台常驻任务：周期性打印 Hello World"""
import threading
import time
from datetime import datetime
from .config import CONSOLE_INTERVAL


def console_loop(stop_event: threading.Event):
    """控制台主循环，直到 stop_event 被设置"""
    counter = 0
    print(f"[Console] 控制台任务已启动，每 {CONSOLE_INTERVAL}s 打印一次。", flush=True)
    while not stop_event.is_set():
        counter += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[Console #{counter}] Hello World!  运行时间 {now}", flush=True)
        # 用 wait 实现可被中断的 sleep
        stop_event.wait(timeout=CONSOLE_INTERVAL)
    print("[Console] 控制台任务已停止。", flush=True)
