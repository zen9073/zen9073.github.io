# Pyenv

## python

```sh
# 安装依赖库
sudo apt install -y build-essential zlib1g-dev libffi-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev

# 安装 pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src

# 设置环境变量
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# 通过中国镜像安装指定版本
export v=3.10.12
wget https://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/
pyenv install $v
pyenv global  $v

# 设置 pip 中国镜像
mkdir -p ~/.pip
cat <<EOF> ~/.pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF

# 更新包管理器
pip install --upgrade pip
pip install --upgrade setuptools
```

## ruby

```sh
git clone https://github.com/rbenv/rbenv.git $HOME/.zen/opt/rbenv

# ruby
export RBENV_ROOT="$HOME/.zen/opt/rbenv"
export PATH=${RBENV_ROOT}/bin:$PATH
eval "$(rbenv init -)"

mkdir -p "$(rbenv root)"/plugins
git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-doctor | bash

rbenv install 2.6.6
rbenv global 2.6.6
```

## nodejs

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/dist

nvm install 20
nvm use 20

curl -fsSL https://get.pnpm.io/install.sh | sh -
curl -fsSL https://get.pnpm.io/install.sh | env PNPM_VERSION=8.10.2 sh -
```
