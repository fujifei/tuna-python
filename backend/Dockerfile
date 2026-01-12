FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 pyca 插件（用于覆盖率上报）
RUN pip install --no-cache-dir git+https://github.com/fujifei/pyca.git

# 安装 coverage 工具
RUN pip install --no-cache-dir coverage

# 设置环境变量（可通过 docker-compose 覆盖）
ENV PYTHONUNBUFFERED=1

# 暴露端口（API 和 Admin 端口）
EXPOSE 8712 8713

# 注意：代码将从 GitHub 拉取，不再使用 COPY
# 默认命令（可以通过 docker-compose 覆盖）
CMD ["python", "api/main.py"]
