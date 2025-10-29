# Docker

## 安装

通过国内镜像手动安装

- <https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/>

或者使用脚本自动完成

```sh
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

手动通过华为镜像安装

```sh
sudo apt install curl gnupg2 ca-certificates lsb-release ubuntu-keyring

curl https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu/gpg | gpg --dearmor \
	| sudo tee /etc/apt/trusted.gpg.d/docker-ce.gpg >/dev/null

sudo add-apt-repository "deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get install docker-ce python3-docker

sudo apt-mark hold docker-buildx-plugin docker-ce docker-ce-cli docker-ce-rootless-extras docker-compose-plugin python3-docker

```

## 参数

```sh
cat << EOF > /etc/docker/daemon.json
{
  "features": {
    "buildkit": true
  },
  "exec-opts": [
    "native.cgroupdriver=systemd"
  ],
  "log-driver": "json-file",
  "log-level": "info",
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
