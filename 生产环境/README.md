# 生产环境部署说明

## 架构说明

```
用户浏览器 → Nginx (端口80) → Flask WSGI (127.0.0.1:5000) → MySQL (3306)
```

## Windows 本地部署方案

Windows 上 gunicorn 和 systemd 不兼容，采用等效替代：

| Linux 组件 | Windows 替代 | 说明 |
|---|---|---|
| gunicorn | waitress | 纯 Python WSGI 服务器，Windows 原生支持 |
| systemd | NSSM + Windows 服务 | 开机自启、崩溃自动重启 |
| Nginx | Nginx Windows 版 | 反向代理 + 静态资源 |

### Windows 部署步骤

1. **安装 waitress**
   ```powershell
   .venv\Scripts\activate
   pip install waitress
   ```

2. **测试启动**
   双击运行 `windows\start-prod.bat`

3. **安装 Nginx Windows 版**
   - 下载: https://nginx.org/en/download.html
   - 将 `windows\nginx.conf` 复制到 Nginx 安装目录的 `conf\` 下

4. **安装为 Windows 服务（开机自启）**
   - 下载 NSSM: https://nssm.cc/download，解压到 `C:\nssm\`
   - 管理员运行 PowerShell:
   ```powershell
   cd 生产环境\windows
   .\install-service.ps1
   ```

5. **访问**
   - Nginx 入口: http://localhost/
   - 直连 Flask: http://localhost:5000/

---

## Linux 服务器部署方案（未来上服务器用）

| 文件 | 作用 |
|---|---|
| `linux\deploy.sh` | 一键部署脚本 |
| `linux\gunicorn_config.py` | gunicorn 配置（worker 数、日志） |
| `linux\water-plant.service` | systemd 服务（开机自启、崩溃重启） |
| `linux\nginx.conf` | Nginx 反向代理配置 |

### Linux 部署步骤

```bash
# 将项目上传到服务器 /opt/water-plant
cd /opt/water-plant
sudo bash 生产环境/linux/deploy.sh
```

### 常用运维命令

```bash
# 查看服务状态
systemctl status water-plant

# 重启服务
systemctl restart water-plant

# 查看实时日志
journalctl -u water-plant -f
```

---

## 目录结构

```
生产环境/
├── README.md                    # 本说明
├── windows/                     # Windows 部署方案
│   ├── requirements-prod.txt    # 生产依赖
│   ├── run_prod.py               # 生产启动入口（waitress）
│   ├── start-prod.bat            # 手动启动脚本
│   ├── nginx.conf                # Nginx 配置
│   └── install-service.ps1       # 安装为 Windows 服务
└── linux/                       # Linux 部署方案
    ├── deploy.sh                 # 一键部署脚本
    ├── requirements.txt          # 生产依赖
    ├── gunicorn_config.py        # gunicorn 配置
    ├── water-plant.service       # systemd 服务
    └── nginx.conf                # Nginx 配置
```
