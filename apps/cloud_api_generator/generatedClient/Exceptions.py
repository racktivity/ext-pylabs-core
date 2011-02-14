import exceptions

class CloudApiException(exceptions.Exception):
    def __init__(self, exception):
        msg = self.handleException(exception)
        self.errmsg = msg
        self.args = (msg,)

    def handleException(self, exception):
        return str(exception).replace('\\n', '\n').replace("\\'", "'")
