# Nginx

# 安装

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

## 主配置

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

## SSL 配置

当前使用的比较安全的 SSL 配置。

```ini
# ssl-options.conf

ssl_protocols TLSv1.2 TLSv1.3; # Requires nginx >= 1.13.0 else use TLSv1.2
ssl_prefer_server_ciphers on;
#ssl_dhparam /etc/nginx/dhparam.pem; # openssl dhparam -out /etc/nginx/dhparam.pem 4096
ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
ssl_session_timeout  10m;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off; # Requires nginx >= 1.5.9
ssl_stapling on; # Requires nginx >= 1.3.7
ssl_stapling_verify on; # Requires nginx => 1.3.7
resolver 8.8.8.8 1.1.1.1 valid=300s;
resolver_timeout 5s;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
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
    listen      80;
    listen      443 ssl http2;
    server_name wiki.9073.me;
    charset     utf-8;

    # force https-redirects
    if ($scheme = http) {
        return 301 https://$server_name$request_uri;
    }

    include     ssl-certificate.conf;
    include     ssl-options.conf;

    access_log  /var/log/nginx/wiki.access.log main;
    error_log   /var/log/nginx/wiki.error.log;

    root /var/www/wiki;

    location / {
        index index.html;
    }

}

```

## 目录权限

设置 /var/www 目录下的文件权限

```bash
mkdir -p /var/www
chown -R nginx:www-data /var/www
chmod 755 /var/www
find /var/www -type d -exec chmod 755 {} +
find /var/www -type f -exec chmod 644 {} +
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
    autoindex on;
    autoindex_localtime on;
    autoindex_exact_size off;
}
```
