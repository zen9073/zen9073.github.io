#!/bin/bash

executable() {
    for x in /s6/*; do
        [[ -f $x/run ]] && chmod +x $x/run
        [[ -f $x/finish ]] && chmod $x/finish
    done
}

pre_passwd() {
    # 确认密码文件
    [[ -f "/etc/ocserv/passwd" ]] || echo 9073 | ocpasswd -c /etc/ocserv/passwd zen
}

pre_cert() {
    # 确认证书文件
    cd /etc/ocserv/
    [[ -f "server.crt" && -f "server.key" ]] ||
        openssl req -new -x509 -nodes -days 3650 \
            -newkey ec:<(openssl ecparam -name prime256v1) \
            -subj "/CN=example.com." \
            -keyout server.key \
            -out server.crt
}

pre_vpn() {
    # 确认虚拟网卡
    if [ ! -e /dev/net/tun ]; then
        mkdir -p /dev/net
        mknod /dev/net/tun c 10 200
        chmod 600 /dev/net/tun
    fi

    # 启用 IPv4 转发
    echo 1 >/proc/sys/net/ipv4/ip_forward

    # 设置 iptables nat 网络转发
    iptables -t nat -A POSTROUTING -j MASQUERADE
    iptables -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
}

executable
pre_passwd
pre_cert
pre_vpn

exec "$@"
