import base64 #used to encode and decode in base64 format
import hashlib
from Crypto.Cipher import AES #import what we downloaded which was pycrytodome

class AES256: #allows the use of any AES including ours which is AES-128
    def __init__(self,key): #key is our password; __init__ initializes the class
        self.key = hashlib.sha256(key.encode()).digest() #generate encryption off the key; .encode is converting string to bytes to pass to hashlib.sha256() function; hashlib.sha256 operate on bytes instead of string; hashlib.sha256(): This creates a SHA-256 hash object; .digest()takes the final hashed value of key and turns it into bytes
        #.encode uses UTF-8 to convert; hashlib.sha256() performs a cryptographic hash function (SHA-256) on those bytes. The result is a fixed-size, irreversible, and secure hash value. ; .digest() is just standard to make sure the hash byte value is the same even if we use a different hash function
        self.iv=b'\xac\xee\xde\x1d\xa0r\xdf\xd2#\xf5\xa8\x8c\x99&\x0b)' #in terminal i generated 16 random bytes by going to python>import os>os.urandom(16) and copying it into the iv
        #b is a prefix indicates a bytes literal; An Initialization Vector is a random or pseudo-random value used in cryptographic algorithms, especially in block cipher modes of operation like Cipher Block Chaining (CBC).
        #ensure that the same plaintext input does not result in the same ciphertext output; iv is used in AES encryption; must be 16 bytes long to fit AES (advanc encryption standard) in CBC (cipher block chaining) mode
    def encrypt(self,plaintext): #this takes plaintext which is my actual password; encrypt is a method in the AES class
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv) #CBC is the mode we are using to encrypt; cipher is a system or algorithm for encrypting and decrypting information; In the context of cryptography, a cipher is a method used to transform plaintext (readable data) into ciphertext (unreadable data) and vice versa. 
        #two types of ciphers: symmetric-key cryptography, the same key is used for both encryption and decryption; Public-key cryptography uses a pair of keys: a public key for encryption and a private key for decryption
        #create an AES cipher object (cipher) using the AES.new function; CBC uses XOR btwn plaintext and iv. for the subsequent blocks, it is XOR'ed btwn prev next plaintext and prev ciphertext; iv is for randomization
        #AES.new function accepts 3 main parameters; we have to define what mode of AES we are using; we are using AES-128 so 16 bytes for both iv and key; cipher right now then is an  object, an instance of the AESCipher class
        padding_length = 16 - (len(plaintext) % 16) #for extra security; this determines how much more padding is needed to make the byte 16 long (the block size for AES in CBC mode)
        plaintext += chr(padding_length) * padding_length #add padding to plaintext; taking the padding length calculated the chr turns the integer of padding_length into a string in the form of unicode characters and times it how ever many times for it to make a block of characters in multiples of 16 for AES encryption to take place

        ciphertext = cipher.encrypt(plaintext.encode()) #actual encryption takes place; The encrypt() method is called on the cipher object. they take the converted bytes and encrypt it using AES in CBC mode; everything is then assigned to the varaible ciphertext
        return base64.b64encode(self.iv + ciphertext) #we concatenate iv and ciphertext; concatenation of the IV with the ciphertext is a common practice for ease of handling during transmission or storage; The base64.b64encode() function in Python is used to encode binary data into a Base64-encoded ASCII string
    
    def decrypt(self, ciphertext):  #adding decryption which is basically reversing what we did up top
        ciphertext = base64.b64decode(ciphertext) #takes a Base64-encoded ASCII string and converts it back into its original binary

        iv = ciphertext[:16] #ciphertext[:16] uses Python slicing to extract the first 16 bytes of the ciphertext byte sequence.
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        plaintext = cipher.decrypt(ciphertext[16:]).decode() #ciphertext[16:] extracts a portion of the ciphertext starting from the 17th byte (index 16) onwards; .decode() is used to convert the resulting decrypted bytes into a Unicode string.
        padding_length = ord(plaintext[-1]) #remove padding and decrypt; plaintext[-1] refers to the last character of the decrypted plaintext. Since the ciphertext was padded before encryption, the last character is expected to represent the padding length; ord() is a built-in Python function that returns the Unicode code point of a given character.
        return plaintext[:-padding_length]
