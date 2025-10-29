# Tailscale

## 安装

手动安装

```sh
sudo apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring

curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/$(lsb_release -cs).noarmor.gpg \
  | sudo tee /etc/apt/trusted.gpg.d/tailscale.gpg >/dev/null

sudo add-apt-repository "deb [arch=amd64] https://pkgs.tailscale.com/stable/ubuntu $(lsb_release -cs) main"

# 发行版文件 例如 noble

wget "https://pkgs.tailscale.com/stable/ubuntu/dists/$(lsb_release -cs)/InRelease"

# all 架构的索引文件链接
wget "https://pkgs.tailscale.com/stable/ubuntu/dists/$(lsb_release -cs)/main/binary-all/Packages"
# amd64 架构的索引文件链接
wget "https://pkgs.tailscale.com/stable/ubuntu/dists/$(lsb_release -cs)/main/binary-amd64/Packages"

# 1.90.4 版本 tailscale 文件直接链接
wget https://pkgs.tailscale.com/stable/ubuntu/pool/tailscale_1.90.4_amd64.deb

# 1.35.181 版本 tailscale-archive-keyring 文件直接链接
wget https://pkgs.tailscale.com/stable/ubuntu/pool/tailscale-archive-keyring_1.35.181_all.deb

sudo apt install ./*.deb
```
