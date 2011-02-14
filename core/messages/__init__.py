import string

def toolStripNonAsciFromText(text):
    return string.join([char for char in str(text) if ((ord(char)>31 and ord(char)<127) or ord(char)==10)],"")