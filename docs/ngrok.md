# ngrok 动态域名服务

下载编译环境

```
apt-get install build-essential golang git
```

获取代码

```
git clone https://github.com/inconshreveable/ngrok.git ngrok
cd ngrok
```

替换为自签名证书

```
cp ca.crt assets/client/tls/ngrokroot.crt
cp 9073.me.crt assets/server/tls/snakeoil.crt
cp 9073.me.key assets/server/tls/snakeoil.key
```

编译 64 位 Linux 服务器端

```
GOOS=linux GOARCH=amd64  make release-server
```

编译各系统环境客户端

```
GOOS=darwin GOARCH=amd64  make release-client
GOOS=windows GOARCH=amd64 make release-client
GOOS=windows GOARCH=386 make release-client
GOOS=linux GOARCH=amd64  make release-client
GOOS=linux GOARCH=386  make release-client
```

配置域名

将 `9073.me` 和 `t[0-9]+.9073.me` 域名指向服务器 IP

服务器端启动

```
mv ngrokd /usr/local/bin/
ngrokd -domain="9073.me" -httpAddr="" -httpsAddr="192.168.1.120:443" -tunnelAddr=":20000"
```

长期使用需要 supervisor

```
[program:ngrokd]
directory = /usr/local/bin/
command = ngrokd -domain="9073.me" -tunnelAddr=":20000" -httpAddr="" -httpsAddr="192.168.1.120:443"
autostart = true
startsecs = 5
autorestart = true
startretries = 3

```

nginx 配置

对外网卡：`192.168.1.10`

对内网卡：`192.168.1.120`

```
server {
    listen      192.168.1.10:443 ssl;
    server_name ~^t[0-9]+\.9073\.me$;
    charset     utf-8;

    ssl_certificate     /etc/ssl/9073/9073.me.crt;
    ssl_certificate_key /etc/ssl/9073/9073.me.key;

    location / {
        proxy_pass https://192.168.1.120:443;
    }
}
```

可以确保 [t0-t20].9073.me 域名可以被 nginx 解析，直接发送到 ngrok 服务。

将 ngrok 客户端复制到 bin 目录然后添加以下客户端配置文件内容

```
cat<< EOF >~/.ngrok
server_addr: 9073.me:20000
trust_host_root_certs: true
tunnels:
  test:
    proto:
      https: 80
    subdomain: t2
EOF
ngrok start test
```

这样可以获取到的全 URL 是 https://t2.9073.me 没有 3 级域名，也没有其他端口

更多使用

```
ngrok --help
```
