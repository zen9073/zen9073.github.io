# Docker

## 安装

通过国内镜像手动安装

- https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/

或者使用脚本自动完成

```sh
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

## 参数

```sh
cat << EOF > /etc/docker/daemon.json
{
  "features": {
    "buildkit": true
  },
  "storage-driver": "overlay2",
  "exec-opts": [
    "native.cgroupdriver=systemd"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "30m",
    "max-file": "2"
  }
}
EOF
```

## 权限

桌面环境还需要添加用户到 docker 组

```sh
usermod -aG docker zen
```
