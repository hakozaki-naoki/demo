#!/bin/bash

# 读取 .env 到环境变量
set -a
[ -f .env ] && source .env
set +a

echo "✅ 开始启动服务..."

# 在后台启动ASR服务
echo "启动ASR服务..."
cd /app/api4sensevoice
python3 server_wss.py &
cd /app

# 启动主服务
echo "启动主服务..."
cd /app
python3 -m uvicorn service.main:app --host 0.0.0.0 --port 8101
