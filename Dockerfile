# Twitter监控器 Docker镜像
# 支持Linux环境运行

FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 安装Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY *.py .
COPY assets/ ./assets/
COPY drivers/ ./drivers/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建非root用户
RUN useradd -m -u 1000 twittermonitor \
    && chown -R twittermonitor:twittermonitor /app

# 切换到非root用户
USER twittermonitor

# 设置环境变量
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# 暴露端口（如果需要）
EXPOSE 8080

# 启动命令
CMD ["python", "main.py"]
