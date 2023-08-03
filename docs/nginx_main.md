# Nginx 安装

基于我常用的 ubuntu 或者 debian 这两个 Linux 发行版安装 mainline 版简略过程。

```bash
distribution=$(lsb_release -si)
codename=$(lsb_release -sc)

sudo apt install -y --no-install-recommends curl gnupg2 ca-certificates lsb-release

echo "deb [arch=amd64] http://nginx.org/packages/mainline/${distribution,,} ${codename,,} nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

curl -fsSL https://nginx.org/keys/nginx_signing.key \
    | sudo apt-key add -

sudo apt update && sudo apt install nginx

sudo usermod -aG www-data nginx
```

# 主配置

根据长期使用最最终版配置。

```ini
# config for nginx
user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;

error_log  /var/log/nginx/error.log;
pid        /var/run/nginx.pid;

events {
    worker_connections  65535;
}

stream {
    resolver 8.8.8.8;
    log_format main '$remote_addr [$time_local] '
                    '$protocol [$ssl_preread_protocol $ssl_preread_server_name] $status $bytes_sent $bytes_received '
                    '$session_time "$upstream_addr" '
                    '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';
    access_log  /var/log/nginx/stream.access.log  main;
    include /etc/nginx/stream/*.conf;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile           on;
    tcp_nopush         on;
    tcp_nodelay        on;

    keepalive_timeout  180;

    gzip               on;
    gzip_vary          on;
    gzip_comp_level    6;
    gzip_buffers       16 8k;
    gzip_min_length    1000;
    gzip_proxied       any;
    gzip_disable       "msie6";
    gzip_http_version  1.0;
    gzip_types         text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript;

    server_names_hash_bucket_size 64;
    server_tokens off;

    include /etc/nginx/conf.d/*.conf;
}
```
