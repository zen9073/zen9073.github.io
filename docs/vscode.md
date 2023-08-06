# VS Code

## 安装

浏览器下载地址 [code.deb](https://go.microsoft.com/fwlink/?LinkID=760868) 。

```shell
sudo apt-get install wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

sudo apt install apt-transport-https
sudo apt update
sudo apt install code # or code-insiders
```

## 插件

```shell
extensions='
esbenp.prettier-vscode
foxundermoon.shell-format
hashicorp.terraform
ms-azuretools.vscode-docker
MS-CEINTL.vscode-language-pack-zh-hans
ms-python.isort
ms-python.python
ms-python.vscode-pylance
ms-toolsai.jupyter
ms-toolsai.jupyter-keymap
ms-toolsai.jupyter-renderers
ms-toolsai.vscode-jupyter-cell-tags
ms-toolsai.vscode-jupyter-slideshow
ms-vscode-remote.remote-containers
ms-vscode-remote.remote-ssh
ms-vscode-remote.remote-ssh-edit
ms-vscode.remote-explorer
redhat.ansible
redhat.vscode-yaml
'

for x in ${extensions}; do
    code --install-extension $x
done
```

## settings 和 snippets

```
settings.json -> /home/zen/.zen/etc/vscode/settings.json
snippets -> /home/zen/.zen/etc/vscode/snippets
```
