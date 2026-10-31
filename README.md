# 水厂主体软件

一套基于 Python 的常驻服务，包含：
- **控制台任务**：后台线程周期性打印 Hello World
- **内置 Web 站点**：Flask 提供，访问 http://127.0.0.1:5000
- **MySQL 数据库**：自动建库 `water_plant` 和测试表 `test`

## 环境信息

| 组件 | 版本 | 位置 |
|---|---|---|
| Python | 3.13.16 | 系统 Python |
| Flask | 3.1.3 | .venv 虚拟环境 |
| PyMySQL | 1.2.3 | .venv 虚拟环境 |
| MySQL | 9.1.0 Community | C:\mysql |
| 数据库 | water_plant | root / root @ 127.0.0.1:3306 |

## 目录结构

```
z主题软件开发/
├── main.py              # 主入口（同时启动控制台 + Web）
├── requirements.txt
├── 启动.bat              # 一键启动脚本
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py        # 数据库 / Web 配置
│   ├── db.py            # 建库建表、增删查
│   ├── console.py        # 控制台循环任务
│   ├── web.py           # Flask 路由
│   └── templates/
│       └── index.html    # 首页（Hello Web + 表单）
└── .venv/               # Python 虚拟环境
```

## 启动方式

**双击 `启动.bat`** 即可。脚本会自动：
1. 检查并启动 MySQL（C:\mysql\bin\mysqld.exe）
2. 启动主程序 main.py

启动后：
- 控制台每 2 秒打印一次 `[Console #n] Hello World! 运行时间 ...`
- 浏览器打开 http://127.0.0.1:5000 看到 "Hello Web"
- 在页面表单输入名称和内容，点"写入数据库"即可向 `test` 表插入一条记录，页面下方会显示最近 10 条记录

## test 表结构

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT AUTO_INCREMENT PK | 主键 |
| name | VARCHAR(50) | 名称 |
| content | VARCHAR(255) | 内容 |
| created_at | DATETIME DEFAULT NOW() | 创建时间 |

## 手动启动命令

```powershell
# 1. 启动 MySQL（如果未运行）
Start-Process "C:\mysql\bin\mysqld.exe" -ArgumentList "--console" -WindowStyle Hidden

# 2. 激活虚拟环境并启动主程序
.venv\Scripts\Activate.ps1
python main.py
```

## IDE

VS Code 安装包可从 https://code.visualstudio.com 下载（winget 安装在本机不稳定，建议手动下载安装）。
