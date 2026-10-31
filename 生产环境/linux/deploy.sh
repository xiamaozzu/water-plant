# ============================================
# 生产环境部署脚本（Linux 服务器）
# 适用: Ubuntu / CentOS / Debian
# 用法: sudo bash deploy.sh
# ============================================

set -e

APP_NAME="water-plant"
APP_DIR="/opt/$APP_NAME"
PYTHON_BIN="python3"

echo "=========================================="
echo "  水厂主体软件 - Linux 生产部署"
echo "=========================================="

# 1. 安装系统依赖
echo "[1/6] 安装系统依赖..."
apt update -y && apt install -y python3-venv python3-pip nginx mysql-server

# 2. 创建虚拟环境并安装依赖
echo "[2/6] 安装 Python 依赖..."
cd $APP_DIR
$PYTHON_BIN -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r 生产环境/linux/requirements.txt

# 3. gunicorn 配置
echo "[3/6] 配置 gunicorn..."
# gunicorn_config.py 已随项目提供

# 4. systemd 服务
echo "[4/6] 配置 systemd 服务..."
cp 生产环境/linux/water-plant.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable water-plant
systemctl restart water-plant

# 5. Nginx 配置
echo "[5/6] 配置 Nginx..."
cp 生产环境/linux/nginx.conf /etc/nginx/sites-available/water-plant
ln -sf /etc/nginx/sites-available/water-plant /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# 6. 完成
echo "[6/6] 部署完成！"
echo "  Web 地址: http://服务器IP/"
echo "  服务管理: systemctl status water-plant"
echo "  日志查看: journalctl -u water-plant -f"
