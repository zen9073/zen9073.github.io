# PVE 安装

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
