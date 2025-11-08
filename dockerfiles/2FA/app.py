import base64
import urllib.parse
import sys
import io
import os
from flask import Flask, render_template_string, request, send_file
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from PIL import Image
from pyzbar.pyzbar import decode as zbar_decode

# 确保导入了 Protobuf 编译生成的模块
try:
    from OtpMigration_pb2 import MigrationPayload
except ImportError:
    print("错误：请确保 OtpMigration_pb2.py 文件存在且可导入。", file=sys.stderr)
    sys.exit(1)

# 确保 Base32 编码库已导入
try:
    import base64 as _base64
except ImportError:
    _base64 = None

# 二维码生成库
import qrcode
from qrcode.image.pil import PilImage

app = Flask(__name__)

# --- 核心功能函数 (为简洁省略，它们保持不变) ---
# 请确保以下函数存在于您的 app.py 中：
# secret_to_base32, generate_otpauth_uri, decode_migration_uri, 
# parse_single_otpauth_uri, construct_otpauth_uri, decode_qrcode_image
# 为保证代码完整性和可测试性，这里仅粘贴关键的解码和构造函数。

def secret_to_base32(secret_bytes):
    """将 Protobuf 字节流密钥转换为标准的 Base32 字符串（用于 otpauth:// URI）。"""
    if _base64 is None:
        return "BASE32_CONVERSION_FAILED"
    return _base64.b32encode(secret_bytes).decode('utf-8').replace('=', '')

def generate_otpauth_uri(otp_param):
    """将单个 OtpParameters 对象转换为标准的 otpauth:// URI。"""
    otp_type_str = "totp"
    if otp_param.type == otp_param.OTP_TYPE_HOTP:
        otp_type_str = "hotp"
    issuer = otp_param.issuer.strip()
    name = otp_param.name.strip()
    label = name
    if issuer and not name.startswith(issuer + ":"):
        label = f"{issuer}:{name}"
    safe_label = urllib.parse.quote(label)
    secret_key_base32 = secret_to_base32(otp_param.secret)
    params = {'secret': secret_key_base32,}
    if issuer: params['issuer'] = issuer
    if otp_type_str == "hotp": params['counter'] = str(otp_param.counter)
    if otp_param.digits == otp_param.DIGIT_COUNT_EIGHT: params['digits'] = '8'
    query_string = urllib.parse.urlencode(params)
    return f"otpauth://{otp_type_str}/{safe_label}?{query_string}"

def decode_migration_uri(uri_string):
    """解码 Google Authenticator 迁移 URI，并返回结构化数据列表。"""
    if not uri_string.startswith("otpauth-migration://offline?data="): return None
    encoded_data = uri_string.split("otpauth-migration://offline?data=")[1]
    url_decoded_data = urllib.parse.unquote(encoded_data)
    try: binary_data = base64.b64decode(url_decoded_data)
    except Exception: return None
    payload = MigrationPayload()
    try:
        payload.ParseFromString(binary_data)
        return [{'uri': generate_otpauth_uri(otp_param),'issuer': otp_param.issuer,'name': otp_param.name,'secret_base32': secret_to_base32(otp_param.secret),'otp_type': 'HOTP' if otp_param.type == otp_param.OTP_TYPE_HOTP else 'TOTP','counter': otp_param.counter} for otp_param in payload.otp_parameters]
    except Exception as e:
        app.logger.error(f"Protobuf 解析失败: {e}")
        return None

def parse_single_otpauth_uri(otpauth_uri_string):
    """解析单个 otpauth:// URI 字符串，提取关键信息。"""
    if not otpauth_uri_string.startswith("otpauth://"): return None
    try:
        parts = urllib.parse.urlparse(otpauth_uri_string)
        otp_type = parts.hostname
        label_full = urllib.parse.unquote(parts.path.lstrip('/'))
        issuer = ""; name = label_full
        if ':' in label_full:
            potential_issuer, potential_name = label_full.split(':', 1)
            if potential_issuer.strip():
                issuer = potential_issuer.strip()
                name = potential_name.strip()
            else: name = label_full.strip()
        else: name = label_full.strip()
        query_params = urllib.parse.parse_qs(parts.query)
        secret = query_params.get('secret', [None])[0]
        if 'issuer' in query_params: issuer = query_params.get('issuer', [issuer])[0]
        if not secret: return None
        return [{'uri': otpauth_uri_string,'issuer': issuer,'name': name,'secret_base32': secret,'otp_type': otp_type.upper(),'counter': query_params.get('counter', [None])[0]}]
    except Exception as e:
        app.logger.error(f"解析单个 otpauth URI 失败: {e}")
        return None

def construct_otpauth_uri(otp_type, issuer, name, secret_base32):
    """根据用户提供的四个字段构造标准的 otpauth:// URI。"""
    otp_type = otp_type.lower()
    if otp_type not in ['totp', 'hotp']: return None, "类型必须是 TOTP 或 HOTP"
    if not secret_base32: return None, "密钥 (Base32) 不能为空"
    label = name.strip()
    if issuer.strip() and not name.strip().startswith(issuer.strip() + ":"): label = f"{issuer.strip()}:{name.strip()}"
    safe_label = urllib.parse.quote(label)
    params = {'secret': secret_base32.strip().upper(),}
    if issuer.strip(): params['issuer'] = issuer.strip()
    if otp_type == "hotp": params['counter'] = '0' 
    query_string = urllib.parse.urlencode(params)
    full_uri = f"otpauth://{otp_type}/{safe_label}?{query_string}"
    return [{'uri': full_uri,'issuer': issuer,'name': name,'secret_base32': secret_base32.strip().upper(),'otp_type': otp_type.upper(),'counter': '0' if otp_type == 'hotp' else ''}], None

def decode_qrcode_image(image_file):
    """解码二维码图片文件，返回解析后的数据列表和错误信息。"""
    try:
        img = Image.open(image_file)
        decoded_objects = zbar_decode(img)
        
        if not decoded_objects:
            return None, "图片中未检测到有效的二维码。"
        
        decoded_data = decoded_objects[0].data.decode('utf-8')
        
        if decoded_data.startswith("otpauth://"):
            return parse_single_otpauth_uri(decoded_data), None
        else:
            return None, f"二维码内容不是有效的 OTP URI，而是: {decoded_data}"

    except Exception as e:
        app.logger.error(f"二维码图片解码失败: {e}")
        return None, f"文件处理错误。请确认文件是有效的图片。错误信息: {e}"


# --- Flask 路由和视图 ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """主页路由：接收输入和展示结果。"""
    results = None
    error = None
    
    # 用于保留输入的变量，以便回显
    migration_uri_input = ""
    single_otp_uri_input = ""
    manual_type = "TOTP"
    manual_issuer = ""
    manual_name = ""
    manual_secret = ""
    selected_mode = "MIGRATION" # 默认选中的模式

    if request.method == 'POST':
        # 1. 从 POST 请求中获取所有可能的输入数据和当前选中的模式
        selected_mode = request.form.get('input_mode', 'MIGRATION').strip().upper()
        
        migration_uri_input = request.form.get('migration_uri', '').strip()
        single_otp_uri_input = request.form.get('single_otp_uri', '').strip()
        
        # 手动输入项
        manual_type = request.form.get('manual_type', 'TOTP').strip().upper()
        manual_issuer = request.form.get('manual_issuer', '').strip()
        manual_name = request.form.get('manual_name', '').strip()
        manual_secret = request.form.get('manual_secret', '').strip()
        
        qr_image_file = request.files.get('qr_image')

        # 2. 根据选中的模式进行处理
        if selected_mode == "MIGRATION" and migration_uri_input:
            results = decode_migration_uri(migration_uri_input)
            if results is None:
                error = "解码 Google Authenticator 迁移 URI 失败。请检查输入的 URI 是否完整且正确。"
                
        elif selected_mode == "SINGLE" and single_otp_uri_input:
            results = parse_single_otpauth_uri(single_otp_uri_input)
            if results is None:
                error = "解析单个 OTP URI 失败。请检查输入的 URI 格式是否正确 (例如: otpauth://totp/LABEL?secret=...)"

        elif selected_mode == "IMAGE" and qr_image_file and qr_image_file.filename:
            if not qr_image_file.mimetype.startswith('image/'):
                 error = "上传的文件不是有效的图片格式。"
            else:
                 results, decode_error = decode_qrcode_image(qr_image_file)
                 if results is None:
                     error = decode_error

        elif selected_mode == "MANUAL" and manual_secret:
            results, error = construct_otpauth_uri(manual_type, manual_issuer, manual_name, manual_secret)
        
        else:
            # 处理模式选中但输入为空的情况
            if selected_mode == "MIGRATION":
                error = "请粘贴 Google Authenticator 迁移 URI 字符串。"
            elif selected_mode == "SINGLE":
                error = "请粘贴单个 OTP URI 字符串。"
            elif selected_mode == "IMAGE":
                error = "请选择一个图片文件上传。"
            elif selected_mode == "MANUAL":
                error = "请输入密钥 (Base32) 和其他必要信息。"
            else:
                error = "请选择一个处理模式。"


    # HTML 模板：引入了 JavaScript 和新的结构
    template = """
    <!doctype html>
    <html lang="zh-CN">
    <head>
        <meta charset="utf-8">
        <title>Google Authenticator / OTP URI 解码工具</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 1200px; margin: auto; }
            h1 { color: #333; }
            form { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9; }
            textarea { width: 100%; min-height: 80px; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; resize: vertical; margin-bottom: 10px; }
            input[type="submit"] { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 20px; }
            input[type="submit"]:hover { background-color: #0056b3; }
            .error { color: red; font-weight: bold; margin-bottom: 15px; border: 1px solid red; padding: 10px; background: #ffe6e6; border-radius: 4px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; word-break: break-all; }
            th { background-color: #f2f2f2; }
            .uri-cell { font-size: 0.8em; }
            .input-group { border: 1px dashed #ccc; padding: 15px; border-radius: 4px; margin-top: 15px; }
            .manual-input-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px; }
            .manual-input-grid input[type="text"] { padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;}
            .manual-input-grid label { font-weight: bold; display: block; margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Google Authenticator / OTP URI 解码工具</h1>
        
        <form method="POST" enctype="multipart/form-data">
            
            <label for="input_mode" style="font-weight: bold; font-size: 1.1em; display: block; margin-bottom: 10px;">请选择输入方式：</label>
            <select id="input_mode" name="input_mode" onchange="showMode(this.value)" style="padding: 10px; border: 1px solid #007bff; border-radius: 4px; width: 100%; max-width: 400px; margin-bottom: 20px;">
                <option value="MIGRATION">1. 解码 Google 迁移 URI (多个账户)</option>
                <option value="SINGLE">2. 解码单个 OTP URI 字符串</option>
                <option value="IMAGE">3. 解码二维码图片</option>
                <option value="MANUAL">4. 手动填写信息 (生成 URI/QR)</option>
            </select>
            
            <hr style="border-top: 1px solid #eee;">

            <div id="mode_MIGRATION" class="input-group">
                <label for="migration_uri">请输入 Google Authenticator 迁移 URI 字符串：</label><br>
                <textarea id="migration_uri" name="migration_uri" rows="5" 
                          placeholder="例如: otpauth-migration://offline?data=ClIKFG1mI%2BEkYtm4d5o1KvgnnDhdz5%2FiEhN6ZW45MDczQGhvdG1haWwuY29tGgpDbG91ZGZsYXJlIAEoATACQhMzYzE4MDExNjk5OTY2OTQxNjky...等">{{ migration_uri_input }}</textarea><br>
            </div>

            <div id="mode_SINGLE" class="input-group" style="display:none;">
                <label for="single_otp_uri">请输入单个 OTP URI 字符串：</label><br>
                <textarea id="single_otp_uri" name="single_otp_uri" rows="3" 
                          placeholder="例如: otpauth://totp/Example:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Example">{{ single_otp_uri_input }}</textarea><br>
            </div>
            
            <div id="mode_IMAGE" class="input-group" style="display:none;">
                <label for="qr_image">选择二维码图片文件 (.png, .jpg)：</label><br>
                <input type="file" id="qr_image" name="qr_image" accept="image/*"><br>
            </div>

            <div id="mode_MANUAL" class="input-group" style="display:none;">
                <label>手动填写信息以生成 URI 和二维码：</label>
                <div class="manual-input-grid">
                    <div>
                        <label for="manual_type">类型 (TOTP/HOTP)</label>
                        <input type="text" id="manual_type" name="manual_type" value="{{ manual_type }}" placeholder="TOTP 或 HOTP" required>
                    </div>
                    <div>
                        <label for="manual_issuer">发行商 (Issuer)</label>
                        <input type="text" id="manual_issuer" name="manual_issuer" value="{{ manual_issuer }}" placeholder="如 Google">
                    </div>
                    <div>
                        <label for="manual_name">账户名 (Name)</label>
                        <input type="text" id="manual_name" name="manual_name" value="{{ manual_name }}" placeholder="如 user@example.com">
                    </div>
                    <div>
                        <label for="manual_secret">密钥 (Base32)</label>
                        <input type="text" id="manual_secret" name="manual_secret" value="{{ manual_secret }}" placeholder="密钥，如 JBSWY3DPEHPK3PXP" required>
                    </div>
                </div>
                <small style="color: #666;">*密钥为必填项。</small>
            </div>

            <input type="submit" value="处理并生成/解码">
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% elif results %}
            <h2>解码/构造结果 (共 {{ results|length }} 个账户)</h2>
            <table>
                <tr>
                    <th>#</th>
                    <th>类型</th>
                    <th>发行商 (Issuer)</th>
                    <th>账户名 (Name)</th>
                    <th>密钥 (Base32)</th>
                    <th>OTP URI</th> 
                    <th>二维码</th>
                </tr>
                {% for item in results %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ item.otp_type }} {% if item.otp_type == 'HOTP' and item.counter %} (计数器: {{ item.counter }}) {% endif %}</td>
                    <td>{{ item.issuer }}</td>
                    <td>{{ item.name }}</td>
                    <td><small>{{ item.secret_base32 }}</small></td>
                    <td class="uri-cell">{{ item.uri }}</td> 
                    <td>
                        <img src="{{ url_for('qrcode_img', uri=item.uri) }}" alt="QR Code" width="150" height="150">
                    </td>
                </tr>
                {% endfor %}
            </table>
        {% endif %}

        <footer>
            <p style="margin-top: 50px; text-align: center; font-size: 0.8em; color: #888;">注意：此工具用于本地解码、构造和恢复您的 2FA 密钥。请勿将密钥分享给他人。</p>
        </footer>
        
        <script>
            // JavaScript 函数，用于根据选择的模式显示/隐藏输入框
            function showMode(mode) {
                var modes = ['MIGRATION', 'SINGLE', 'IMAGE', 'MANUAL'];
                modes.forEach(function(id) {
                    var element = document.getElementById('mode_' + id);
                    if (element) {
                        element.style.display = (id === mode) ? 'block' : 'none';
                    }
                });
                
                // 确保在 POST 失败回显时，正确的模式仍然被选中
                var selectElement = document.getElementById('input_mode');
                if (selectElement) {
                    selectElement.value = mode;
                }
            }
            
            // 页面加载完成后，设置默认选中模式
            window.onload = function() {
                // 根据后端传来的 selected_mode 变量来初始化显示
                var initialMode = "{{ selected_mode }}";
                showMode(initialMode);
            };
        </script>
    </body>
    </html>
    """
    
    # 确定在 POST 失败回显时，哪个模式应该被再次选中
    current_mode_to_display = selected_mode
    if results is None and error is None and request.method != 'POST':
        # GET 请求，使用默认值
        current_mode_to_display = "MIGRATION"
    elif results or error:
        # POST 请求结束，保持当前模式，以便用户可以看到他们的输入
        current_mode_to_display = selected_mode

    return render_template_string(template, 
                                  results=results, 
                                  error=error, 
                                  migration_uri_input=migration_uri_input, 
                                  single_otp_uri_input=single_otp_uri_input,
                                  manual_type=manual_type,
                                  manual_issuer=manual_issuer,
                                  manual_name=manual_name,
                                  manual_secret=manual_secret,
                                  selected_mode=current_mode_to_display)

@app.route('/qrcode', methods=['GET'])
def qrcode_img():
    # ... (此函数保持不变) ...
    uri = request.args.get('uri')
    if not uri:
        return "URI 参数缺失", 400

    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4, 
            border=2,
        )
        
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"生成二维码失败: {e}")
        return "生成二维码失败", 500

if __name__ == '__main__':
    # 请确保您已经安装了所有依赖，特别是 pyzbar 的系统依赖 libzbar-dev
    app.run(host='0.0.0.0', debug=True)