import base64
from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings
import hashlib
import hmac
import os

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class CipherManager:
    def __init__(self):        
        self.key = hmac.new(bytes(os.environ.get('ENC_KEY').encode('utf-8')), msg=settings.SECRET_KEY.encode('utf-8'), digestmod=hashlib.sha256).digest()[:BS]

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return str(base64.b64encode( iv + cipher.encrypt( raw ) ),'utf-8' )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return str(unpad(cipher.decrypt( enc[16:] )),'utf-8')


class JIRACipher(CipherManager):
    pass


class EmailCipher(CipherManager):
    pass        
        