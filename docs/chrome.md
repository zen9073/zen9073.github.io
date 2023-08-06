# Chrome

## 下载

在快捷链接页面 [Google Chrome](links.md) 包含了各平台的下载地址。

```she
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

## 必装插件

1. 去除烦人的广告 [Adblock Plus](https://chrome.google.com/webstore/detail/cfhdojbkjhnklbpkdaibdccddilifddb?utm_source=chrome-app-launcher-info-dialog)
2. 方便的密码管家 [LastPass](https://chrome.google.com/webstore/detail/hdokiejnpimakedhajhdlcegeplioahd?utm_source=chrome-app-launcher-info-dialog)
3. 国内的网络必备 [Proxy SwitchyOmega](https://chrome.google.com/webstore/detail/padekgcemlokbadohgkifijomclgjgif?utm_source=chrome-app-launcher-info-dialog)

## Google Search

### 让 Google 搜索不跳转到 .hk 页面

在地址栏输入 `https://www.google.com/ncr` 然后只要不清空 cookie 就会一直有效。

### 使用 www.google.com 搜索

打开 `chrome://settings/searchEngines` 页面，先选择使用其他，然后删除 `Google`,再新建 `Google Search Engine` 内容就使用下面的链接填充。

英文搜索 `https://www.google.com/search?hl=en&q=%s`

中文搜索 `https://www.google.com/search?hl=zh-CN&q=%s`
