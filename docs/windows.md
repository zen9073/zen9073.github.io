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

slmgr.vbs /skms 192.168.1.1

slmgr.vbs /ato
```

## Offfice 2016 KMS 激活步骤

```bat
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

## 删除 windwos 10/11 的库

```
Windows Registry Editor Version 5.00

[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{088e3905-0323-4b02-9826-5d99428e115f}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{0DB7E03F-FC29-4DC6-9020-FF41B59E513A}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{1CF1260C-4DD0-4ebb-811F-33C572699FDE}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{24ad3ad4-a569-4530-98e1-ab02f9417aa8}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{374DE290-123F-4565-9164-39C4925E467B}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{3ADD1653-EB32-4cb0-BBD7-DFA0ABB5ACCA}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{3dfdf296-dbec-4fb4-81d1-6a3438bcf4de}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{A0953C92-50DC-43bf-BE83-3742FED03C9C}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{A8CDFF1C-4878-43be-B5FD-F8091C1C60D0}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{d3162b92-9365-467a-956b-92703aca08af}]
[-HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{f86fa3ab-70d2-4fc7-9c99-fcbf05467f3a}]
```

## 在此处打开命令窗口

```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\background\shell\OpenCMDHere]
@="在此处打开命令窗口"
"Icon"="cmd.exe"
"ShowBasedOnVelocityId"=dword:00639bc8

[HKEY_CLASSES_ROOT\Directory\background\shell\OpenCMDHere\command]
@="cmd.exe /s /k pushd \"%V\""
```

## 删除顽固文件

```bat
DEL /F /A /Q \\?\%1
RD /S /Q \\?\%1
```
