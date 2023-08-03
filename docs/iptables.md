# iptables 开机恢复预设配置

## 预设配置

```shell
cat <<EOF >/etc/iptables.rulesets
*filter

#  Allow all loopback (lo0) traffic and drop all traffic to 127/8 that doesn't use lo0
-A INPUT -i lo -j ACCEPT
-A INPUT -d 127.0.0.0/8 -j REJECT

#  Accept all established inbound connections
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#  Allow all outbound traffic - you can modify this to only allow certain traffic
-A OUTPUT -j ACCEPT

#  Allow HTTP and HTTPS connections from anywhere (the normal ports for websites and SSL).
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT

#  Allow SSH connections
#
#  The -dport number should be the same port number you set in sshd_config
#
-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT

#  Allow ping
-A INPUT -p icmp -j ACCEPT

#  Log iptables denied calls
-A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

#  Drop all other inbound - default deny unless explicitly allowed policy
-A INPUT -j DROP

COMMIT
EOF
```

## 启动后自动恢复

服务脚本

```shell
cat <<EOF >/lib/systemd/system/boot-restore-iptables.service
[Unit]
Description = Apply iptables rules

# 设置在 ssh 之后启动，
# 因为在系统启动到一定阶段 iptables-restore 才能有效，
# 然而具体的信息暂时不确定，
After = ssh.service

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'iptables-restore < /etc/iptables.rulesets'
RemainAfterExit=yes

[Install]
WantedBy=default.target
EOF
```

启用服务

```shell
systemctl enable boot-restore-iptables.service
```
