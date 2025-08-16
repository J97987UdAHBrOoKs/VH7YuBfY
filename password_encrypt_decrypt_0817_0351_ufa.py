# 代码生成时间: 2025-08-17 03:51:54
import cherrypy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import binascii

"""
Password Encryption and Decryption Tool using Python and CherryPy framework.
"""

class PasswordTool:
    def __init__(self):
        # AES key (16, 24, or 32 bytes)
        self.key = get_random_bytes(16)  # 128-bit key
        self.iv = get_random_bytes(AES.block_size)  # Initialization vector

    def encrypt(self, plaintext):
        """
        Encrypts a plaintext string using AES encryption.
        :param plaintext: The string to be encrypted.
        :return: A base64 encoded encrypted string.
        """
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            padded_data = pad(plaintext.encode(), AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}")

    def decrypt(self, encrypted_text):
        """
        Decrypts an encrypted string using AES decryption.
        :param encrypted_text: The base64 encoded encrypted string to be decrypted.
        :return: The decrypted plaintext string.
        """
        try:
            encrypted_data = base64.b64decode(encrypted_text)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            padded_data = cipher.decrypt(encrypted_data)
            return unpad(padded_data, AES.block_size).decode()
        except (ValueError, binascii.Error) as e:
            raise ValueError(f"Decryption failed: {e}")

    @cherrypy.expose
    def encrypt_password(self, input_text):
        """
        Exposes an endpoint to encrypt a password.
        :param input_text: The password to be encrypted.
        :return: A JSON response with the encrypted password.
        """
        encrypted = self.encrypt(input_text)
        return {
            "status": "success",
            "encrypted_password": encrypted
        }

    @cherrypy.expose
    def decrypt_password(self, encrypted_text):
        """
        Exposes an endpoint to decrypt a password.
        :param encrypted_text: The encrypted password to be decrypted.
        :return: A JSON response with the decrypted password.
        """
        try:
            decrypted = self.decrypt(encrypted_text)
            return {
                "status": "success",
                "decrypted_password": decrypted
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }

if __name__ == '__main__':
    config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    app = PasswordTool()
    cherrypy.quickstart(app, config=config)
