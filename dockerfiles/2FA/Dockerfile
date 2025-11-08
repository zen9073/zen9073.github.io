FROM python:3.13.4


# 设置非交互式
ARG DEBIAN_FRONTEND=noninteractive

# 使用中国时区
ENV TZ=Asia/Shanghai

# 使用国内源
RUN sed -i 's/[a-z]*\.[a-z]*\.[a-z]*/repo.huaweicloud.com/' /etc/apt/sources.list.d/debian.sources

# 安装 apt 
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends libzbar-dev \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app
COPY . /app

# 安装 pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
