```
command = /opt/ngrok/ngrokd -domain="ngrok.9073.me" -tunnelAddr="192.168.1.180:4443" -httpsAddr="192.168.1.182:443" -httpAddr="" -tlsKey="/etc/nginx/ssl/dev.key" -tlsCrt="/etc/nginx/ssl/dev.crt"
```

```config
cat ~/.ngrok

server_addr: ngrok.9073.me:4443
trust_host_root_certs: true
tunnels:
  zen:
    proto:
      https: 9090
    subdomain: zen
```

```
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
ExecStart=/opt/ngrok/ngrokd -domain="ngrok.9073.me" -tunnelAddr="192.168.200.180:4443" -httpsAddr="192.168.200.182:443" -httpAddr="" -tlsKey="/opt/ngrok/ngrok.key" -tlsCrt="/opt/ngrok/ngrok.crt"
ExecStop=/bin/kill -HUP $MAINPID
PrivateTmp=True
#Restart=always
Restart=on-failure


[Install]
WantedBy=multi-user.target

```