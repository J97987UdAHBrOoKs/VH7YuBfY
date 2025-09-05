# 代码生成时间: 2025-09-05 18:34:09
import cherrypy
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto import Random

# 初始化AES密钥
# 这里使用SHA256哈希函数生成密钥
key = SHA256.new(b'your_password_key').digest()

# AES块大小
block_size = 16

# 加密函数
def encrypt(plaintext):
    """
    将明文进行AES加密

    :param plaintext: 明文字符串
    :return: 加密后的Base64编码字符串
    """
    # 随机生成一个盐值
    salt = Random.new().read(block_size)
    # 初始化加密器
    cipher = AES.new(key, AES.MODE_CBC, salt)
    # 填充明文
    padded_plaintext = pad(plaintext.encode('utf-8'), block_size)
    # 加密明文
    ciphertext = cipher.encrypt(padded_plaintext)
    # 将盐值和密文组合并进行Base64编码
    return base64.b64encode(salt + ciphertext).decode('utf-8')

# 解密函数
def decrypt(ciphertext):
    """
    将密文进行AES解密

    :param ciphertext: 加密后的Base64编码字符串
    :return: 解密后的明文字符串
    """
    # Base64解码
    decoded_ciphertext = base64.b64decode(ciphertext)
    # 提取盐值
    salt = decoded_ciphertext[:block_size]
    # 提取密文
    encrypted_plaintext = decoded_ciphertext[block_size:]
    # 初始化解密器
    cipher = AES.new(key, AES.MODE_CBC, salt)
    # 解密密文
    padded_plaintext = cipher.decrypt(encrypted_plaintext)
    # 去除填充
    plaintext = unpad(padded_plaintext, block_size).decode('utf-8')
    return plaintext

# 暴露加密和解密接口
class PasswordTool:
    exposed = True

    @cherrypy.expose
    def index(self):
        return 'Welcome to the Password Tool!'

    @cherrypy.expose
    def encrypt_password(self, plaintext):
        """
        暴露加密接口

        :param plaintext: 明文字符串
        :return: 密文字符串
        """
        if not plaintext:
            return 'Input cannot be empty.'
        return encrypt(plaintext)

    @cherrypy.expose
    def decrypt_password(self, ciphertext):
        """
        暴露解密接口

        :param ciphertext: 密文字符串
        :return: 明文字符串
        """
        try:
            return decrypt(ciphertext)
        except (ValueError, KeyError):
            return 'Invalid ciphertext.'

# 配置CherryPy
config = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    },
}

if __name__ == '__main__':
    cherrypy.quickstart(PasswordTool(), config=config)