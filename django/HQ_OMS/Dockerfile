# 基础镜像：Python 3.13.5-slim（与你的配置一致，轻量且兼容）
FROM python:3.13.5-slim

# 安装系统依赖（MySQL 驱动必需）
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录（容器内固定路径，不是上传的文件内）
WORKDIR /app

# 【新增优化】创建静态文件目录并授权（避免 collectstatic 时权限报错）
RUN mkdir -p /app/staticfiles && chmod 755 /app/staticfiles

# 更新 pip 并安装 Python 依赖（--no-cache-dir 减少镜像体积）
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝 Django 项目文件（本地 HQ_OMS 目录所有文件拷贝到容器 /app）
COPY . .

# 环境变量（适配项目名 HQ_OMS，确保群辉里的 Django 加载正确配置）
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=HQ_OMS.settings

# 暴露容器内端口（正确，仅内部网络可见，与 docker-compose 适配）
EXPOSE 8000

# 默认启动命令（docker-compose 会覆盖此命令执行 migrate/collectstatic，此处作备用）
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "HQ_OMS.wsgi:application"]