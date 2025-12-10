# PostgreSQL

## 安装

通过国内镜像手动安装

- <https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/>

```sh
sudo apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring

curl https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt/ACCC4CF8.asc \
 | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/postgresql.gpg >/dev/null

sudo add-apt-repository "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/apt $(lsb_release -cs)-pgdg main"

sudo apt update

# client
sudo apt install -y postgresql-client-18 postgresql-client-common libpq-dev

# server
sudo apt install -y postgresql-18

# pgvector
sudo apt install -y postgresql-18-pgvector
```

## 认证

```sh
touch ~/.pgpass
chmod 0600 ~/.pgpass
echo "127.0.0.1:5432:*:postgres:password" >> ~/.pgpass
```
