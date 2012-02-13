
CODEX='utf-8'

class Text:

    def toStr(self, value, codex=CODEX):
        if isinstance(value, str):
            return value
        elif isinstance(value, unicode):
            return value.encode(codex)
        else:
            return str(value)

    def toUnicode(self, value, codex=CODEX):
        if isinstance(value, str):
            return value.decode(codex)
        elif isinstance(value, unicode):
            return value
        else:
            return unicode(value)


