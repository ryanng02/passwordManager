import base64
import hashlib
from Crypto.Cipher import AES #import what we downloaded which was pycrytodome

class AES256:
    def __init__(self,key): #key is our password
        self.key = hashlib.sha256(key.encode()).digest() #generate encryption off the key
        self.iv=b'\xac\xee\xde\x1d\xa0r\xdf\xd2#\xf5\xa8\x8c\x99&\x0b)' #in terminal i generated 16 random bytes by going to python>import os>os.urandom(16) and copying it into the iv

    def encrypt(self,plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv) #CBC is the mode we are using to encrypt

        padding_length = 16 - (len(plaintext) % 16) #for extra security
        plaintext += chr(padding_length) * padding_length #add padding to plaintext

        ciphertext = cipher.encrypt(plaintext.encode())
        return base64.b64encode(self.iv + ciphertext)
    
    def decrypt(self, ciphertext):  #adding decryption which is basically reversing what we did up top
        ciphertext = base64.b64decode(ciphertext)

        iv = ciphertext[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        plaintext = cipher.decrypt(ciphertext[16:]).decode()
        padding_length = ord(plaintext[-1]) #remove padding and decrypt
        return plaintext[:-padding_length]