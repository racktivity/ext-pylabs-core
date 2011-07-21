#Handle RAW connection with the emulator
from racktivity.common import convert

def Connect(username, password, hostname="127.0.0.1", port=8080, format="R"):
    return BlockingConnection(username, password, hostname, port, format)

class BlockingConnection(object):
    def __init__(self, username, password, hostname="127.0.0.1", port=8080, format="R"):
        import urllib
        url = "http://%s:%s@%s:%s" % (username, password, hostname, port)
        self.get_url = url + "/API.cgi?ADDR=%(addr)s&GUID=%(guid)s&TYPE=G"
        self.set_url = url + "/API.cgi?ADDR=%(addr)s&GUID=%(guid)s&TYPE=S"
        self.urllib = urllib
    
    def getAttribute(self, module, guid, port=1, length=1):
        url = self.get_url % {"addr": module, "guid": guid}
        if port > 1:
            url = url + "&INDEX=" + str(port)
        if length > 1:
            url = url + "&COUNT=" + str(length)
        data = self._send_data(url)
        return data[:-2]
    
    def setAttribute(self, module, guid,value, port=1):
        if isinstance(value, bool):
            value = int(value)
        url = self.set_url % {'addr': module, "guid": guid}
        if port > 1:
            url = url + "&INDEX=" + str(port)
        
        #Add the encoded value
        url = url + "&LEN=%d"%len(value)
        url = url + "&" + self.urllib.urlencode({"DATA":value})
        #, "data": self.urllib.quote(str(value))
        data = self._send_data(url)
        return data[:-2]
    
    def _send_data(self, url):
        url_f = self.urllib.urlopen(url)
        data = url_f.read()
        url_f.close()
        if url_f.code != 200:
            raise RuntimeError("Server fault code %s message %s" % (url_f.code, data))
        return data