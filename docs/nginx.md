# Nginx

## 安装

基于我常用的 ubuntu 或者 debian 这两个 Linux 发行版安装 mainline 版简略过程。

```bash
# 1. 使用原生方式获取变量 (无需依赖 lsb-release)
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_DISTRO=$ID               # ubuntu 或 debian
    OS_CODENAME=$VERSION_CODENAME # noble 或 bookworm
fi

# 2. 安装基础依赖
sudo apt update
sudo apt install -y --no-install-recommends \
    curl gnupg2 ca-certificates lsb-release ubuntu-keyring

# 3. 创建目录并处理密钥 (使用 --dearmor 确保是二进制格式)
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /etc/apt/keyrings/nginx-archive-keyring.gpg >/dev/null

# 4. 写入 DEB822 格式配置 (推荐方式)
cat <<EOF | sudo tee /etc/apt/sources.list.d/nginx.sources
Types: deb
URIs: https://nginx.org/packages/mainline/${OS_DISTRO}
Suites: ${OS_CODENAME}
Components: nginx
Architectures: amd64
Signed-By: /etc/apt/keyrings/nginx-archive-keyring.gpg
EOF

# 5. 安装
sudo apt update
sudo apt install -y nginx
sudo usermod -aG www-data nginx
```

## 主配置

根据长期使用最最终版配置。

```ini
# config for nginx
user nginx;
worker_processes auto;
worker_cpu_affinity auto; # 针对大小核架构的绑定优化
worker_rlimit_nofile 65535;

error_log  /var/log/nginx/error.log warn; # 生产环境建议 warn 级别
pid        /var/run/nginx.pid;

events {
    use epoll; # 显式指定 Linux 下性能最好的 epoll
    worker_connections  65535;
    multi_accept on; # 让每个 worker 一次性接受所有新连接
}

stream {
    resolver 119.29.29.29 223.5.5.5 valid=300s;
    resolver_timeout 5s;

    log_format main '$remote_addr [$time_local] '
                    '$protocol [$ssl_preread_protocol $ssl_preread_server_name] $status $bytes_sent $bytes_received '
                    '$session_time "$upstream_addr" '
                    '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
    access_log  /var/log/nginx/stream.access.log  main;

    # 确保文件夹存在，否则 Nginx 启动会报错
    include /etc/nginx/stream/*.conf;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    # 性能优化
    sendfile           on;
    tcp_nopush         on;
    tcp_nodelay        on;
    keepalive_timeout  180;
    reset_timedout_connection on; # 释放超时的死连接，保护内存

    # 现代 Gzip 配置
    gzip               on;
    gzip_vary          on;
    gzip_comp_level    5; # 6 和 5 性能损耗比差别大，但压缩率接近，5 更平衡
    gzip_min_length    1024;
    gzip_proxied       any;
    gzip_types         text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # 安全与限制
    server_names_hash_bucket_size 64;
    server_tokens off; # 隐藏版本号，默认建议关闭

    include /etc/nginx/conf.d/*.conf;
}
```

## SSL 配置

当前使用的比较安全的 SSL 配置。

```ini
# ssl-options.conf

# [2026 Modern SSL Configuration]
# Optimized for Ubuntu 24.04 (Noble) & OpenSSL 3.0+
# Note: OCSP Stapling is intentionally removed as per Let's Encrypt 2025/2026 standards.

# 1. 协议选择：强制 TLS 1.2/1.3，优先 1.3
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off; # TLS 1.3 协商机制更安全，建议设为 off

# 2. 加密套件：针对你的 ECC 证书和 Alder Lake (AES-NI) 优化
# 优先使用 ECDSA + AES-GCM 算法
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

# 3. 曲线优化：加入 X25519 (目前最快的椭圆曲线)
ssl_ecdh_curve X25519:secp384r1:prime256v1;

# 4. 会话管理：提高复用率以减少握手耗时
ssl_session_timeout  1d;
ssl_session_cache shared:SSL:10m; # 约可缓存 40,000 个会话
ssl_session_tickets off;          # 为了 Perfect Forward Secrecy (PFS) 建议关闭

# 5. 性能跃迁：开启 TLS 1.3 0-RTT (可选)
# 注意：0-RTT 存在重放攻击风险，仅建议在幂等请求（GET）较多的场景开启
# ssl_early_data on;

# 6. 安全响应头 (HSTS & 防御增强)
# 开启 HSTS，有效期 2 年，包含子域名并允许预加载
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options SAMEORIGIN always;
add_header X-Content-Type-Options nosniff always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
# 内容安全策略：根据实际需求调整，此处为基础加固
add_header Content-Security-Policy "upgrade-insecure-requests" always;

# 7. 移除已失效的 OCSP 配置
# 已删除: ssl_stapling, ssl_stapling_verify, ssl_trusted_certificate
# 2025 年 8 月 6 日 - Let's Encrypt 关闭 OCSP 服务器
```

## 证书配置

```ini
# ssl-certificate.conf

ssl_certificate     /etc/nginx/ssl/server.crt;
ssl_certificate_key /etc/nginx/ssl/server.key;
```

## https

```ini
server {
    listen 80;
    listen [::]:80;
    server_name example.org;

    # 高性能 HTTP -> HTTPS 重定向
    return 301 https://$host$request_uri;
}

server {
    # 开启 HTTP/2 和 HTTP/3 (QUIC)
    listen 443 ssl http2;
    listen 443 quic reuseport; # HTTP/3 端口
    listen [::]:443 ssl http2;
    server_name example.org;
    charset     utf-8;

    # 证书引用
    include     ssl-certificate.conf;
    # 加载通用加密选项
    include     ssl-options.conf;
    # 告知浏览器支持 HTTP/3
    add_header Alt-Svc 'h3=":443"; ma=86400';

    access_log  /var/log/nginx/wiki.access.log main;
    error_log   /var/log/nginx/wiki.error.log warn;

    # 站点路径
    root /var/www/wiki;
    index index.html;

    location / {
        try_files $uri $uri/ =404;

        # 针对 0-RTT 的安全加固
        proxy_set_header Early-Data $ssl_early_data;
    }

    # 屏蔽隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

}

```

## 目录权限

设置 /var/www 目录下的文件权限

```bash
mkdir -p /var/www
chown -R nginx:www-data /var/www
chmod 2755 /var/www
find /var/www -type d -exec chmod 2755 {} +
find /var/www -type f -exec chmod 0644 {} +
```

## robots.txt

如果不希望被索引，还可以设置 robots.txt，告诉爬虫不要抓取。

```ini
# robots.txt generated at http://portal.qiniu.com
User-agent: Baiduspider
Disallow: /
User-agent: Sosospider
Disallow: /
User-agent: sogou spider
Disallow: /
User-agent: YodaoBot
Disallow: /
User-agent: Googlebot
Disallow: /
User-agent: Bingbot
Disallow: /
User-agent: Slurp
Disallow: /
User-agent: MSNBot
Disallow: /
User-agent: googlebot-image
Disallow: /
User-agent: googlebot-mobile
Disallow: /
User-agent: yahoo-blogs/v3.9
Disallow: /
User-agent: psbot
Disallow: /
User-agent: *
Disallow: /
```

2026 年推荐的“极简私人”版

```
# example.org - Private Repository
User-agent: *
Disallow: /

# 禁止 AI 训练爬虫 (2026 年新增核心需求)
User-agent: GPTBot
Disallow: /
User-agent: CCBot
Disallow: /
```

## 配合 Nginx 的“二次防御”

由于很多流氓爬虫会伪造 User-agent 或者根本不遵守 robots.txt，既然你刚才配置了高性能的 Nginx，建议在 conf 中加入针对 UA 的过滤：

```ini
# 在 server 块中加入
if ($http_user_agent ~* (Baiduspider|Sogou|Yisou|Bytespider)) {
    return 403;
}
```

## basic 验证

```sh
sudo apt install -y apache2-utils
htpasswd -bc passwd user pass
```

```ini
    auth_basic          "passwd";
    auth_basic_user_file passwd;
```

## 开启索引

```ini
location / {
    # --- 开启目录索引 ---
    autoindex           on;
    autoindex_localtime on;   # 显示服务器本地时间
    autoindex_exact_size off; # 显示 KB/MB/GB (更易读)
}
```
