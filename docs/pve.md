# Proxmox VE

## mirror

<https://mirrors.tuna.tsinghua.edu.cn/proxmox/iso/>

<https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/jammy/current/>

<https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso>

## install

自主分区：

- swap 0
- root 20G

## PVE server

```sh
sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list

source /etc/os-release
echo "deb https://mirrors.tuna.tsinghua.edu.cn/proxmox/debian $VERSION_CODENAME pve-no-subscription" >>/etc/apt/sources.list

rm /etc/apt/sources.list.d/pve-enterprise.list

apt update && apt full-upgrade -y

apt install aria2 curl wget htop vim iftop iotop tree netcat net-tools -y
```

## kvm Guest

### image

```sh
aria2c -c -x 10 -s 10 https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/jammy/current/jammy-server-cloudimg-amd64.img

qemu-img convert -f qcow2 -O raw jammy-server-cloudimg-amd64.img jammy-server-cloudimg-amd64.raw

fdisk -ul jammy-server-cloudimg-amd64.raw

mkdir -p /raw

mount -o loop,offset=$((227328 * 512)) jammy-server-cloudimg-amd64.raw /raw

sed -i "s@http://.*archive.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g"  /raw/etc/apt/sources.list
sed -i "s@http://.*security.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /raw/etc/apt/sources.list

sed -i "s@http://.*archive.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g"  /raw/etc/cloud/cloud.cfg
sed -i "s@http://.*security.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /raw/etc/cloud/cloud.cfg

umount /raw


```

### create

```sh
# 创建虚拟机
qm create 100

# 导入 cloudimg 文件作为硬盘并设置为启动盘
# qm importdisk 100 jammy-server-cloudimg-amd64.img local-lvm --format qcow2
qm importdisk 100 jammy-server-cloudimg-amd64.raw local-lvm --format raw
qm set 100 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-100-disk-0
qm set 100 --boot c --bootdisk scsi0

# 添加 cloudinit 设置
qm set 100 --ide2 local-lvm:cloudinit
qm set 100 --ciuser root
qm set 100 --sshkey ~/.ssh/authorized_keys

# 添加网卡设置
qm set 100 --net0 virtio,bridge=vmbr0
qm set 100 --ipconfig0 ip=10.10.10.100/24,gw=10.10.10.1

# 添加第二快网卡设置
#qm set 100 --net1 virtio,bridge=vmbr1
#qm set 100 --ipconfig1 ip=10.10.8.100/24

# 其他杂项设置
qm set 100 --serial0 socket --vga serial0
qm set 100 --agent enabled=1,fstrim_cloned_disks=1,type=virtio
qm set 100 --ostype l26
qm set 100 --onboot 1
qm set 100 --cpu host
qm set 100 --name ubuntu

# 设置 CPU 内存 硬盘
qm set 100 --cores 1
qm set 100 --memory 1024
qm resize 100 scsi0 5G

```

## 系统初始化设置

```yaml
- name: kvm
  hosts: all
  gather_facts: false
  vars:
    ansible_python_interpreter: /usr/bin/python3
    basic_tools:
      - build-essential
      - python3-dev
      - python3-pip
      - cron
      - curl
      - git
      - htop
      - iftop
      - iptables
      - man
      - mosh
      - mtr-tiny
      - p7zip-full
      - tree
      - vim
      - vnstat
      - wget
      - zip

  pre_tasks:
    - raw: bash -c "test -e /usr/bin/python3 || (apt -qqy update && apt install -qqy python3)"

  tasks:
    - name: 设置为中国时区
      timezone: name='Asia/Shanghai'

    - name: 设置 bash 命令行提示符为彩色
      lineinfile: dest="~/.bashrc" regexp='^#?force_color_prompt=yes' line='force_color_prompt=yes'

    - name: vim 的自定义配置
      copy: content="syntax on" dest=/root/.vimrc force=yes backup=yes
    - lineinfile:
        path: "/root/.vimrc"
        line: "{{item}}"
      with_items:
        - syntax on
        - hi Comment ctermfg = 6
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

    - name: 启用 ipv4 的转发，并禁用 ipv6
      copy: content="# Automatically generated by Ansible\n" dest=/etc/sysctl.conf force=yes backup=yes
    - lineinfile:
        path: "/etc/sysctl.conf"
        line: "{{item}}"
      with_items:
        - net.ipv4.ip_forward = 1
        - fs.file-max = 262144
        - vm.max_map_count = 262144
        - net.ipv6.conf.all.disable_ipv6 = 1
        - net.ipv6.conf.default.disable_ipv6 = 1
        - net.ipv6.conf.lo.disable_ipv6 = 1

    - name: 调整系统参数
      lineinfile:
        path: "/etc/security/limits.conf"
        line: "{{item}}"
      with_items:
        - "* soft nofile 262144"
        - "* hard nofile 262144"
        - "root soft nofile 262144"
        - "root hard nofile 262144"

    - name: 安装系统更新
      apt: upgrade=full update_cache=yes

    - name: 安装系统基础的应用工具
      apt: name={{basic_tools}} state=present

    - name: 卸载 snap step 1
      shell: "snap remove {{item}}"
      loop:
        - lxd
        - core20
        - snapd
      ignore_errors: yes
    - name: 卸载 snap step 2
      systemd: name=snapd state=stopped
      ignore_errors: yes
    - name: 卸载 snap step 3
      apt: name=snapd state=absent
    - name: 卸载 snap step 4
      file: path=/root/snap state=absent
```