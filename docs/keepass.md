# KeePass

## 安装

```sh
sudo apt install -y keepass2
sudo apt install -y install libcanberra-gtk-module

```

## 中文

- 下载语言包

https://downloads.sourceforge.net/keepass/KeePass-2.44-Chinese_Simplified.zip

- 设置字体

在 KeePass 中，单击 'Tools' → 'Options' → 'Interface'，拉到最下，去掉勾选 'Force usage of system font(Unix only)'，然后单击 'SelectListFont'，选择 'Noto Sans CJK SC' 字体 。

- 设置语言

在 KeePass 中，单击 'View' → 'Change Language' → 'Open Folder' 按钮，可以看到一个目录，下载语言文件然后解压到这个目录。

```shell
sudo mkdir -p /usr/lib/keepass2/Languages
sudo mv Chinese_Simplified.lngx /usr/lib/keepass2/Languages
```

重新打开 KeePass 再单击 'View' → 'Change Language'，选择中文。

然而并不能完全显示中文，还是有部分中文会被显示成框框。

## k2

要完整显示中文需要设置 `zh_CN.UTF-8` 环境。例如，

```shell
export LC_ALL=zh_CN.UTF-8 && keepass2
```

或者直接再 .bashrc 使用 alias。

```shell
alias k2='export LC_ALL=zh_CN.UTF-8 && keepass2'
```
