from pylabs import q
import hashlib
import base64

BLOCKSIZE = 8

class Encryption(object):
    def __init__(self):
        self.__blowfish = None
    
    @property
    def __bw(self):
        if not self.__blowfish:
            from Crypto.Cipher import Blowfish
            nics = filter(lambda x: x.startswith("eth") or x.startswith("wlan"), q.system.net.getNics())
            if not nics:
                raise Exception("No nics found")
            
            nics.sort()
            mac = q.system.net.getMacAddress(nics[0])
            self.__blowfish = Blowfish.new(mac)
            
        return self.__blowfish
    def encrypt(self, word):
        """
        Encrypts the given word so only the decrypt method on the same machine can decrypt it
        """
        extra = (len(word) + 2) % BLOCKSIZE
        padding = 0
        if extra:
            padding = BLOCKSIZE - extra
        
        word = "%d:%s" % (padding, word) + "\0" * padding
        return "___%s" % base64.b64encode(self.__bw.encrypt(word))
    
    def decrypt(self, cypher):
        """
        Decrypt the given cypher returned from the encrypt
        """
        if not cypher.startswith("___"):
            raise ValueError("Invalid cypher")
        cypher = cypher[3:]
        word = self.__bw.decrypt(base64.b64decode(cypher))
        padding, _, word = word.partition(":")
        padding = int(padding)
        if padding:
            word = word[:-padding]
        return word
