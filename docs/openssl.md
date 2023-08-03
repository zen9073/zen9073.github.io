# OpenSSL

## 生成证书

### rsa 证书

同时生成 crt 和 key 证书

```shell
openssl req -new -x509 -nodes -days 3650 \
    -subj "/CN=example.com." \
    -keyout server.key \
    -out server.crt
```

分步生成 crt 和 key 证书

```shell
# key
openssl genrsa -out server.key

# crt
openssl req -new -x509 -days 3650 \
    -key server.key \
    -out server.crt \
    -subj "/CN=example.com."
```

### ec 证书

同时生成 crt 和 key 证书

```shell
openssl req -new -x509 -nodes -days 3650 \
    -newkey ec:<(openssl ecparam -name prime256v1) \
    -subj "/CN=example.com." \
    -keyout server.key \
    -out server.crt
```

分步生成 crt 和 key 证书

```shell
# key
openssl ecparam -genkey -name secp256r1 | openssl ec -out server.key

# crt
openssl req -new -x509 -days 3650 \
    -key server.key \
    -out server.crt \
    -subj "/CN=example.com."
```

### 第三方签发

生成 csr 文件提交给第三方签发证书。

```shell
openssl req -new -key server.key -out server.csr -subj "/CN=example.com."
```

## 查看和校验

查看证书信息

```shell
# rsa key
openssl rsa -noout -text -in server.key

# ec key
openssl ec -noout -text -in server.key

# csr
openssl req -noout -text -in server.csr

# crt
openssl x509 -noout -text -in server.crt
```

校验证书是否匹配

```shell
# rsa
diff -eq <(openssl x509 -pubkey -noout -in server.crt) <(openssl rsa -pubout -in server.key)
# 单独输出以下为匹配
writing RSA key

# ec
diff -eq <(openssl x509 -pubkey -noout -in server.crt) <(openssl ec -pubout -in server.key)
# 单独输出以下为匹配
read EC key
writing EC key

# 包含 differ 的输出则为不匹配
```

## 其他

如果要为多个域名或者 IP 签发证书， 则需要在 `-subj` 之外使用 `-addext` 再添加信息，多条信息使用逗号分割。

```shell
# 域名
-addext "subjectAltName = DNS:www.example.com."

# IP
-addext "subjectAltName = IP:1.2.3.4"

# 多条信息
-addext "subjectAltName = DNS:www.example.com.,IP:1.2.3.4"

```
