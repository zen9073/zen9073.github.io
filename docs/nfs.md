# NFS 使用

```sh
# 安装
sudo apt install nfs-common

# 发现
sudo showmount -e 10.10.10.4

#　挂载
sudo mount -t nfs 10.10.10.4:/NAS /mnt

# 开机自动挂载
10.10.10.4:/NAS /mnt nfs defaults 0 0
```

```sh
# nfs version 3 版本
mount -t nfs -vvvv -o nfsvers=3 10.10.10.4:/NFS /nas

10.10.10.4:/NFS /nas nfs defaults,timeo=900,retrans=5,_netdev 0 0
```
