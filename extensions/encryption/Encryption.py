from pylabs import q
import hashlib
from Crypto.Cipher import DES3

BLOCKSIZE = 8

class Encryption(object):
    def __init__(self):
        nics = filter(lambda x: x.startswith("eth") or x.startswith("wlan"), q.system.net.getNics())
        if not nics:
            raise Exception("No nics found")
        
        nics.sort()
        mac = q.system.net.getMacAddress(nics[0])
        md5 = hashlib.md5(mac)
        self.__key = md5.hexdigest()[0:24]
        self.__des3 = DES3.new(self.__key)
        
    def encrypt(self, word):
        """
        Encrypts the given word so only the decrypt method on the same machine can decrypt it
        """
        extra = (len(word) + 2) % BLOCKSIZE
        padding = 0
        if extra:
            padding = BLOCKSIZE - extra
        
        word = "%d:%s" % (padding, word) + "\0" * padding
        return self.__des3.encrypt(word)
    
    def decrypt(self, cypher):
        """
        Decrypt the given cypher returned from the encrypt
        """
        word = self.__des3.decrypt(cypher)
        padding, _, word = word.partition(":")
        padding = int(padding)
        if padding:
            word = word[:-padding]
        return word
