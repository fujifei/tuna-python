#!/bin/bash
# 启动API服务

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# 获取项目根目录（backend 的父目录）
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 激活虚拟环境
source "$PROJECT_ROOT/venv/bin/activate"

# 安装 pyca 插件
pip install git+https://github.com/fujifei/pyca.git@master

cd "$SCRIPT_DIR"

# 读取配置获取端口号
API_PORT=$(python -c "
import sys
import os
# 添加backend目录到路径
sys.path.insert(0, '$SCRIPT_DIR')
from config.config import load_config
cfg = load_config()
print(cfg.api_port)
" 2>/dev/null)

# 如果读取失败，使用默认端口
if [ -z "$API_PORT" ]; then
    API_PORT=8712
    echo "Warning: Failed to read config, using default port $API_PORT"
fi

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -ti:$port >/dev/null 2>&1; then
        return 0  # 端口被占用
    else
        return 1  # 端口未被占用
    fi
}

# 清理占用端口的进程
cleanup_port() {
    local port=$1
    echo "Port $port is in use, cleaning up..."
    
    # 查找占用端口的进程
    local pids=$(lsof -ti:$port 2>/dev/null)
    
    if [ -z "$pids" ]; then
        echo "No process found on port $port"
        return
    fi
    
    # 杀掉占用端口的进程
    for pid in $pids; do
        echo "Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null
    done
    
    # 等待一下确保进程被清理
    sleep 1
    
    # 再次检查
    if check_port $port; then
        echo "Warning: Port $port is still in use after cleanup"
    else
        echo "Port $port has been cleaned up"
    fi
}

# 检查并清理端口
if check_port $API_PORT; then
    cleanup_port $API_PORT
fi

# 启动服务
python api/main.py

