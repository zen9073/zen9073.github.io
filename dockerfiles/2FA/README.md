# Google Authenticator / OTP URI 解码与构造工具

这是一个基于 Python Flask 框架的 Web 应用，旨在提供一个便捷的界面来处理各种两步验证 (2FA) 密钥和 URI。它可以解码 Google Authenticator 的批量迁移 URI，解析单个 OTP URI，并支持通过手动输入密钥或上传二维码图片来生成或提取 2FA 账户信息。

## ✨ 主要功能

1.  **解码 Google 迁移 URI：** 解析 Google Authenticator 生成的 `otpauth-migration://offline?data=...` 字符串，批量恢复所有账户的密钥。
2.  **解码单个 OTP URI：** 解析标准的 `otpauth://` 格式 URI，提取账户详情。
3.  **二维码图片解码：** 上传包含 `otpauth://` 信息的二维码图片，自动解码并显示密钥。
4.  **手动构造 URI/QR：** 允许用户手动输入 `类型`、`发行商`、`账户名` 和 `密钥 (Base32)`，实时生成标准的 OTP URI 和对应的二维码。
5.  **结果展示：** 以清晰的表格形式展示恢复的账户信息（包括类型、发行商、密钥、完整的 OTP URI）和可扫描的二维码图片。

---

## 🚀 部署指南

### 📜 前提条件

您需要在部署环境（Linux/Windows/macOS）中安装以下组件：

1.  **Python 3.8+**
2.  **Git** (可选，用于克隆项目)
3.  **ZBar 系统库** (仅在需要**二维码图片解码**功能时需要)

### 步骤一：安装 ZBar 系统依赖 (仅 Linux/Ubuntu)

如果您计划使用**“解码二维码图片”**功能，必须先安装底层的 ZBar 库。

```bash
# 更新系统包列表
sudo apt update

# 安装 ZBar 开发库
sudo apt install libzbar-dev
```

### 步骤二：项目初始化与 Python 依赖安装

1.  **创建项目目录并进入：**

    ```bash
    mkdir otp-tool
    cd otp-tool
    ```

2.  **创建并激活虚拟环境 (强烈推荐)：**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate   # Windows
    ```

3.  **将 `app.py` 和 `OtpMigration_pb2.py` 放入目录中。**

4.  **安装 Python 依赖库：**

    ```bash
    # 安装 Flask, Protobuf, QRCode, 以及用于图片解码的 Pillow 和 pyzbar
    pip install Flask qrcode[pil] protobuf pyzbar Pillow
    ```

### 步骤三：运行应用

由于应用被配置为监听 `0.0.0.0`，因此您可以在网络中访问它。

1.  **启动 Flask 应用：**

    ```bash
    # 启用调试模式，方便开发和查看日志
    python app.py
    ```

2.  **访问应用：**

    - 应用通常会在端口 `5000` 运行。
    - **本地访问：** `http://127.0.0.1:5000/`
    - **网络访问：** `http://<您的服务器IP地址>:5000/`

    > **注意：** 如果您在云服务器上部署，请确保您的防火墙已开放 TCP 端口 `5000`。

### 步骤四：生产环境部署 (可选)

对于需要长期稳定运行的生产环境，**不推荐**直接使用 `app.run(debug=True)`。您应该使用 Gunicorn, uWSGI 等 WSGI 服务器配合 Nginx/Apache 反向代理。

**使用 Gunicorn 部署示例：**

1.  **安装 Gunicorn：**

    ```bash
    pip install gunicorn
    ```

2.  **启动 Gunicorn 进程：**

    ```bash
    # 使用 4 个工作进程，绑定到所有接口的 5000 端口
    gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
    ```

    _(`app:app` 指的是 `app.py` 文件中的 `app` 实例)_

3.  **配置 Nginx (可选)：** 配置 Nginx 作为反向代理，将外部请求转发到 Gunicorn 监听的 `5000` 端口，并处理 SSL/TLS 加密。

---

## ⚠️ 安全提示

- **密钥安全：** 本工具旨在本地恢复您的 2FA 密钥。请**不要**将您的密钥或迁移 URI 字符串输入到任何您不信任的第三方在线工具中。
- **本地运行：** 建议仅在本地网络或受控环境中运行此工具。
- **数据：** 本应用不会存储任何您输入的数据。所有处理均在内存中完成。
