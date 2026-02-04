#!/bin/bash

# 读取 .env 到环境变量
set -a
[ -f .env ] && source .env
set +a

echo "✅ 开始启动服务..."

# 保存当前目录
CURRENT_DIR=$(pwd)

# 使用 source 激活 Conda 环境
echo "激活 Conda 环境..."
source /opt/anaconda3/bin/activate api4sensevoice

# 检查环境是否激活成功
if [ $? -ne 0 ]; then
    echo "Conda 环境激活失败，尝试创建环境..."
    conda create -n api4sensevoice python=3.8 -y
    source /opt/anaconda3/bin/activate api4sensevoice
fi

# 安装依赖项
echo "安装依赖项..."
pip install funasr
pip install uvicorn
pip install fastapi

# 设置 Python 路径
export PYTHONPATH="$CURRENT_DIR/backend:$PYTHONPATH"

# 在后台启动ASR服务
echo "启动ASR服务..."
cd "$CURRENT_DIR/api4sensevoice"
python3 server_wss.py &

# 返回原目录启动主服务
cd "$CURRENT_DIR"
echo "启动主服务..."
python3 -m uvicorn service.main:app --host 0.0.0.0 --port 8101
