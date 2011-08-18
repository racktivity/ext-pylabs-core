import string

# For backward compatibility with unicode strings, we keep the old version
# around and use it accordingly
def _old_toolStripNonAsciFromText(text):
    return string.join([char for char in str(text) if ((ord(char)>31 and ord(char)<127) or ord(char)==10)],"")


_deletions = range(0, 10) + range(11, 32) + range(127, 255)
_deletionChars = ''.join(chr(c) for c in _deletions)
del _deletions

def toolStripNonAsciFromText(text, _dontUse=_deletionChars):
    if isinstance(text, str):
        return text.translate(None, _dontUse)
    else:
        return _old_toolStripNonAsciFromText(text)
