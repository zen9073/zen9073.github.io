#!/bin/bash

executable() {
    for x in /s6/*; do
        [[ -f $x/run ]] && chmod +x $x/run
        [[ -f $x/finish ]] && chmod $x/finish
    done
}

pre_passwd() {
    # 确认密码文件
    [[ -f "/etc/squid/passwd" ]] || htpasswd -b -c /etc/squid/passwd zen 9073
}

pre_cert() {
    # 确认证书文件
    cd /etc/squid/
    [[ -f "server.crt" && -f "server.key" ]] ||
        openssl req -new -x509 -nodes -days 3650 \
            -newkey ec:<(openssl ecparam -name prime256v1) \
            -subj "/CN=example.com." \
            -keyout server.key \
            -out server.crt
}

executable
pre_passwd
pre_cert

exec "$@"
