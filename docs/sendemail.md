# SendEmail

## 安装

```sh
apt-get install sendemail libio-socket-ssl-perl libnet-ssleay-perl
```

## 使用

```sh
/usr/bin/sendEmail \
-s smtp.mailgun.org:587 \
-o tls=yes \
-xu postmaster@domain \
-xp password \
-f user@domain \
-t another.user@another.domain \
-u "Test" \
-m "ok?"
```
