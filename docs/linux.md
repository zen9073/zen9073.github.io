# Linux

## 远程 windwos 系统

```sh
sudo apt install remmina
```

## 查看 rammina 保存的密码

```sh
apt install seahorse
```

## mkisofs

```sh
mkisofs -r -R -J -l -iso-level 3 xx.iso xx
```

## jq

```sh
cat list | jq ' [ . | to_entries[] | .key=.value.label | .value = .value.location ] | from_entries'
```

## ssh_config

```bash
Host    *
    ServerAliveInterval 10
    ControlPersist      10h
    ControlMaster       auto
    ControlPath         ~/.ssh/%h-%p-%r

Host    100
    Port 22
    User root
    Hostname    192.168.1.100
    IdentityFile ~/.ssh/id_rsa


Host    git.9073.me
    HostName        git.9073.me
    IdentityFile    ~/.ssh/git.key
    IdentitiesOnly  Yes

```

## wget 自动修正文件名

> wget --content-disposition

## chrome 首页被劫持

> chrome: 用记事本打开 C:\Users\zen\AppData\Local\Google\Chrome\User Data\Default\Secure Preferences

## nemo

```sh
#!/bin/bash

new() {
    xdg-mime default nemo.desktop inode/directory application/x-gnome-saved-search
    gsettings set org.gnome.desktop.background show-desktop-icons false
    gsettings set org.nemo.desktop show-desktop-icons true
}

old() {
    gsettings set org.gnome.desktop.background show-desktop-icons true
    gsettings set org.nemo.desktop show-desktop-icons false
    xdg-mime default nautilus.desktop inode/directory application/x-gnome-saved-search
}

#new
#old
```

## cloud init

```yaml
#cloud-config
# vim: syntax=yaml

user: root
disable_root: False
password: rootroot
chpasswd:
  expire: False
apt:
  primary:
    - arches: [amd64]
      uri: http://repo.huaweicloud.com/ubuntu/
  security:
    - uri: http://repo.huaweicloud.com/ubuntu/
      arches: [amd64]
package_update: false
package_upgrade: false
ssh_authorized_keys:
  - ssh-rsa ......
  - ssh-rsa ......
```

```sh
cloud-localds cloud-init.iso cloud-init.yaml
```

## realvnc

```
cmVhbHZuYyA1LnggNi54IAoKQlEyNEctUERYRTQtS0tLUlMtV0JIWkUtRjVSQ0EKQlEyNEctUERYRTQtS0tLUlMtV0JIWkUtRjVSQ0EKOFpFWkgtUVBBTk0tTlgzQTUtOEM0VFMtOEI5N0EKN0FCNFgtM1lOWEYtQzVNUlItNTlESkctN0hHTkEKVVBMOFAtQ04yTVQtODVFUkEtTjNFM0ItR0VSREEKSFJCUkgtM0JONTItWjhFQ0gtQ0o3QjctTU5YM0EKCg==
```