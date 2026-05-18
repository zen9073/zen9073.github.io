# Ngrok

## 编译

下载编译环境

```sh
apt-get install build-essential golang git
```

获取代码

```sh
git clone https://github.com/inconshreveable/ngrok.git ngrok
cd ngrok
```

替换为自签名证书

```sh
cp ca.crt assets/client/tls/ngrokroot.crt
cp example.org.crt assets/server/tls/snakeoil.crt
cp example.org.key assets/server/tls/snakeoil.key
```

编译 64 位 Linux 服务器端

```sh
GOOS=linux GOARCH=amd64  make release-server
```

编译各系统环境客户端

```sh
GOOS=darwin GOARCH=amd64  make release-client
GOOS=windows GOARCH=amd64 make release-client
GOOS=windows GOARCH=386 make release-client
GOOS=linux GOARCH=amd64  make release-client
GOOS=linux GOARCH=386  make release-client
```

## 配置

将 `example.org` 和 `*.example.org` 域名指向服务器 IP，然后配置 nginx。

- 对外网卡：`192.168.1.10`
- 对内网卡：`192.168.1.110`

```ini
server {
    listen      192.168.1.10:443 ssl;
    server_name *.example.org;
    charset     utf-8;

    ssl_certificate     /etc/ssl/example.org.crt;
    ssl_certificate_key /etc/ssl/example.org.key;

    location / {
        proxy_pass https://192.168.1.110:443;
    }
}
```

可以确保 *.example.org 域名可以被 nginx 解析，直接发送到 ngrok 服务。

将 ngrok 客户端复制到 bin 目录然后添加以下客户端配置文件内容

## ngrok client

```yaml
# ~/.ngrok
server_addr: example.org:4443
trust_host_root_certs: false

tunnels:
  web:
    subdomain: web
    proto:
      https: 8888
      http: 8888
  ssh:
    remote_port: 5922
    proto:
      tcp: 22
  vnc:
    remote_port: 5900
    proto:
      tcp: 5900
```

## systemd

```code
#  /etc/systemd/system/ngrokd.service
[Unit]
Description=ngrokd
Wants=network.target
After=syslog.target

[Service]
#Type=forking
Type=simple
#User=nobody
PIDFile=/var/run/ngrokd.pid
ExecStart=/opt/ngrok/ngrokd -domain="example.org" -tunnelAddr="192.168.1.10:4443" -httpsAddr="192.168.1.110:443" -httpAddr="192.168.1.110:80" -tlsKey="/opt/ngrok/ngrok.key" -tlsCrt="/opt/ngrok/ngrok.crt"
ExecStop=/bin/kill -HUP $MAINPID
PrivateTmp=True
#Restart=always
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
