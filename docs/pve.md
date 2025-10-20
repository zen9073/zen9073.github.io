# Proxmox VE

## Mirror

<https://mirrors.tuna.tsinghua.edu.cn/proxmox/iso/>

<https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/noble/current/>

<https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso>

## Install

自主分区：

- swap 0
- ~~root 20G~~

## PVE Server

```sh
# sources pve8
sed -i 's|^deb http://deb.debian.org|deb https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

rm /etc/apt/sources.list.d/ceph.list
rm /etc/apt/sources.list.d/pve-enterprise.list

source /etc/os-release
echo >> /etc/apt/sources.list "deb https://mirrors.tuna.tsinghua.edu.cn/proxmox/debian $VERSION_CODENAME pve-no-subscription"

# sources pve9
sed -i 's|^URIs: http://deb.debian.org|URIs: https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources
sed -i 's|^URIs: http://ftp.debian.org|URIs: https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources
sed -i 's|^URIs: http://security.debian.org|URIs: https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources

rm /etc/apt/sources.list.d/ceph.sources
rm /etc/apt/sources.list.d/pve-enterprise.sources

source /etc/os-release
cat << EOF >/etc/apt/sources.list.d/proxmox.sources
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/proxmox/debian/pve
Suites: $VERSION_CODENAME
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
EOF

# apt
apt update && apt full-upgrade -y
apt install -y aria2 curl wget htop vim iftop iotop tree netcat-openbsd net-tools ifupdown2
apt install -y libgl1 libegl1

# lvm
lvremove /dev/pve/data
lvextend -rl +100%FREE /dev/pve/root
lvs
vgs
pvs
df -hT

# storage
/etc/pve/storage.cfg

# bash
sed -i 's|# zh_CN.UTF-8 UTF-8|zh_CN.UTF-8 UTF-8|' /etc/locale.gen
locale-gen

echo >> ~/.bashrc "export LC_ALL='en_US.UTF-8'"
echo >> ~/.bashrc "PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '"

# vim
cat << EOF >~/.vimrc
syntax on
hi Comment ctermfg=6
let loaded_matchparen=1
set encoding=utf-8
set tabstop=4
set softtabstop=4
set expandtab
set ruler
set showcmd
set showmatch
set hlsearch
set incsearch
EOF
```

## KVM Guest

### Image

```sh
aria2c -c -x 10 -s 10 https://mirrors.huaweicloud.com/ubuntu-cloud-images/noble/current/noble-server-cloudimg-amd64.img
qemu-img convert -f qcow2 -O raw noble-server-cloudimg-amd64.img noble-server-cloudimg-amd64.raw

mkdir -p /raw
# fdisk -ul noble-server-cloudimg-amd64.raw
mount -o loop,offset=$((2099200 * 512)) noble-server-cloudimg-amd64.raw /raw

sed -i "s@http://.*archive.ubuntu.com@http://mirrors.huaweicloud.com@g"  /raw/etc/apt/sources.list.d/ubuntu.sources
sed -i "s@http://.*security.ubuntu.com@http://mirrors.huaweicloud.com@g" /raw/etc/apt/sources.list.d/ubuntu.sources

sed -i "s@http://.*archive.ubuntu.com@http://mirrors.huaweicloud.com@g"  /raw/etc/cloud/cloud.cfg
sed -i "s@http://.*security.ubuntu.com@http://mirrors.huaweicloud.com@g" /raw/etc/cloud/cloud.cfg

umount /raw
```

### Create

```sh
# 创建虚拟机
qm create 101

# 导入 cloudimg 文件作为硬盘
qm importdisk 101 noble-server-cloudimg-amd64.raw hd01 --format raw
qm set 101 --scsihw virtio-scsi-single --scsi0 hd01:101/vm-101-disk-0.raw

# 设置启动盘
qm set 101 --boot c --bootdisk scsi0

# 添加 cloudinit 设置
# qm set 101 --ide2 hd01-lvm:cloudinit
qm set 101 --ide2 hd01:cloudinit,format=raw
qm set 101 --ciuser root
qm set 101 --ciupgrade 0
qm set 101 --sshkey ~/.ssh/authorized_keys

# 添加网卡设置
qm set 101 --net0 virtio,bridge=vmbr0
# qm set 101 --ipconfig0 ip=dhcp
# qm set 101 --ipconfig0 ip=192.168.1.11/24,gw=192.168.1.1

# 其他杂项设置
qm set 101 --serial0 socket --vga serial0
qm set 101 --agent enabled=1,fstrim_cloned_disks=1,type=virtio
qm set 101 --ostype l26
qm set 101 --onboot 1
qm set 101 --cpu host
qm set 101 --name ubuntu

# 设置 CPU 内存 硬盘
qm set 101 --cores 4
qm set 101 --memory 2048
qm resize 101 scsi0 10G
```

## 系统初始化设置

```yaml
- name: PVE
  hosts: all
  gather_facts: false
  vars:
    basic_tools:
      - apache2-utils
      - apt-transport-https
      - aria2
      - bash-completion
      - build-essential
      - ca-certificates
      - cron
      - curl
      - git
      - htop
      - iftop
      - iptables
      - jq
      - man
      - mosh
      - mtr-tiny
      - net-tools
      - p7zip-full
      - python3-dev
      - python3-docker
      - python3-passlib
      - python3-pip
      - p7zip-full
      - qemu-guest-agent
      - software-properties-common
      - tree
      - vim
      - vnstat
      - wget
      - yq
      - zip

  tasks:
    - name: 设置为中国时区
      community.general.timezone:
        name: "Asia/Shanghai"

    - name: 设置 bash 命令行提示符为彩色
      ansible.builtin.lineinfile:
        path: /root/.bashrc
        regexp: "^#?force_color_prompt=yes"
        line: force_color_prompt=yes

    - name: Vim 的自定义配置 | 1
      ansible.builtin.copy:
        content: |
          "syntax on"
        dest: /root/.vimrc
        force: true
        backup: true
        mode: "0644"
    - name: Vim 的自定义配置 | 2
      ansible.builtin.lineinfile:
        path: "/root/.vimrc"
        line: "{{ item }}"
      with_items:
        - syntax on
        - hi Comment ctermfg=6
        - let loaded_matchparen=1
        - set encoding=utf-8
        - set tabstop=4
        - set softtabstop=4
        - set expandtab
        - set ruler
        - set showcmd
        - set showmatch
        - set hlsearch
        - set incsearch

    - name: 启用 ipv4 的转发，并禁用 ipv6 | 1
      ansible.builtin.copy:
        content: |
          # Automatically generated by Ansible\n
        dest: /etc/sysctl.conf
        force: true
        backup: true
        mode: "0644"
    - name: 启用 ipv4 的转发，并禁用 ipv6 | 2
      ansible.builtin.lineinfile:
        path: "/etc/sysctl.conf"
        line: "{{ item }}"
      with_items:
        - net.ipv4.ip_forward = 1
        - fs.file-max = 262144
        - vm.max_map_count = 262144
        - net.ipv6.conf.all.disable_ipv6 = 1
        - net.ipv6.conf.default.disable_ipv6 = 1
        - net.ipv6.conf.lo.disable_ipv6 = 1

    - name: 调整系统参数
      ansible.builtin.lineinfile:
        path: "/etc/security/limits.conf"
        line: "{{ item }}"
      with_items:
        - "* soft nofile 262144"
        - "* hard nofile 262144"
        - "root soft nofile 262144"
        - "root hard nofile 262144"

    - name: 安装系统更新
      ansible.builtin.apt:
        upgrade: full
        update_cache: true

    - name: 安装系统基础的应用工具
      ansible.builtin.apt:
        name: "{{ item }}"
        state: present
      with_items: "{{ basic_tools }}"

    - name: 停用 systemd-resolved
      ansible.builtin.systemd_service:
        name: systemd-resolved
        state: stopped
        enabled: false

    - name: 删除旧的 resolv.conf
      ansible.builtin.file:
        path: /etc/resolv.conf
        state: absent

    - name: 添加新的 resolv.conf
      ansible.builtin.copy:
        content: |
          # Automatically generated by Ansible
          nameserver 114.114.114.114
        dest: /etc/resolv.conf
        mode: "0644"

    - name: 卸载 snap step 1
      community.general.snap:
        name: "{{ item }}"
        state: absent
      loop:
        - lxd
        - core20
        - snapd
    - name: 卸载 snap step 2
      ansible.builtin.systemd_service:
        name: snapd
        state: stopped
    - name: 卸载 snap step 3
      ansible.builtin.apt:
        name: snapd
        state: absent
    - name: 卸载 snap step 4
      ansible.builtin.file:
        path: /root/snap
        state: absent

    - name: 静态路由 | 1
      ansible.builtin.copy:
        content: |
          [Unit]
          # /lib/systemd/system/lan_static.service
          Description = Apply static route rules
          After = ssh.service

          [Service]
          Type=oneshot
          ExecStart=/bin/sh -c 'bash -x /root/route_add.sh'
          RemainAfterExit=yes

          [Install]
          WantedBy=default.target
        dest: /lib/systemd/system/lan_static.service
        mode: "0644"
    - name: 静态路由 | 2
      ansible.builtin.systemd:
        name: lan_static.service
        enabled: true
    - name: 静态路由 | 3
      ansible.builtin.copy:
        content: |
          #!/bin/bash
          set -x
          lan_ip='192.168.0.0/16'
          switch=192.168.99.254
          ip route add $lan_ip via $switch
        dest: /root/route_add.sh
        mode: "0755"

```
