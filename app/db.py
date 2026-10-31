"""数据库连接与初始化"""
import pymysql
from .config import DB_CONFIG


def get_connection():
    """获取一个新的数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def init_database():
    """创建数据库（若不存在）并建 test 表"""
    # 先不指定 database，连到 MySQL 默认实例上建库
    cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = pymysql.connect(**cfg)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` "
                f"DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
    finally:
        conn.close()

    # 再连到目标库建表
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS `test` (
                    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
                    name VARCHAR(50) NOT NULL COMMENT '名称',
                    content VARCHAR(255) NOT NULL COMMENT '内容',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试表'
                """
            )
        conn.commit()
    finally:
        conn.close()


def insert_test(name: str, content: str):
    """向 test 表插入一条记录，返回新插入的 id"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO `test` (name, content) VALUES (%s, %s)"
            cur.execute(sql, (name, content))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_test(limit: int = 10):
    """查询最近的 test 记录"""
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                "SELECT id, name, content, created_at FROM test ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            return cur.fetchall()
    finally:
        conn.close()
