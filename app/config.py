"""全局配置"""
import os

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "water_plant"),
    "charset": "utf8mb4",
}

# Web 配置
WEB_HOST = "127.0.0.1"
WEB_PORT = 5000

# 控制台任务间隔（秒）
CONSOLE_INTERVAL = 2
