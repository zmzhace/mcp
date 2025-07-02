#!/bin/bash

echo "🚀 启动 FastMCP HTTP 服务器..."

# 激活虚拟环境
source .venv/bin/activate

# 启动 HTTP 服务器
python main_http.py 