# Windwos Server 系统常见问题

## 快速添加可以远程的用户

```bat
net user /add user01 Hello2020

net localgroup "Remote Desktop users" /add user01
```

## 激活 server 2019

```bat
DISM /Online /Set-Edition:ServerStandard /ProductKey:N69G4-B89J2-4G8F4-WWYCC-J464C /AcceptEula

slmgr.vbs /ipk N69G4-B89J2-4G8F4-WWYCC-J464C

slmgr.vbs /skms 192.168.200.180

slmgr.vbs /ato
```

# Windwos 系统常见问题

## 删除顽固文件
```shell
   DEL /F /A /Q \\?\%1
   RD /S /Q \\?\%1
```


# Offfice 2016  KMS 激活步骤

```shell
cd /D "C:\Program Files (x86)\Microsoft Office\root\Licenses16"

cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_KMS_Client-ppd.xrm-ms
cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_KMS_Client-ul-oob.xrm-ms
cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_KMS_Client-ul.xrm-ms
cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_MAK-pl.xrm-ms
cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_MAK-ppd.xrm-ms
cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_MAK-ul-oob.xrm-ms
cscript ..\..\office16\ospp.vbs /inslic:ProPlusVL_MAK-ul-phn.xrm-ms

cscript ..\..\office16\ospp.vbs /sethst:192.168.1.1
cscript ..\..\office16\ospp.vbs /inpkey:XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99

cscript ..\..\office16\ospp.vbs /act
cscript ..\..\office16\ospp.vbs /dstatus

cscript ..\..\office16\ospp.vbs /unpkey:BTDRB

```



