
from pylabs.Shell import *
import unicodedata


import pylabs

class String:
    #exceptions = Exceptions
    
    def decodeUnicode2Asci(self,text):
        return unicodedata.normalize('NFKD', text.decode("utf-8")).encode('ascii','ignore')
    