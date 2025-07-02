#!/bin/bash

# 查找并停止MCP服务器进程
echo "正在查找MCP服务器进程..."
PID=$(ps aux | grep "python main.py" | grep -v grep | awk '{print $2}')

if [ -n "$PID" ]; then
    echo "找到MCP服务器进程 (PID: $PID)，正在停止..."
    kill $PID
    echo "MCP服务器已停止"
else
    echo "未找到运行中的MCP服务器进程"
fi 