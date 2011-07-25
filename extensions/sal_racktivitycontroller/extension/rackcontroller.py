from racktivity.sal import client
class RackController(object):
    def connect(self, address, port, login, password, format='R'):
        return client.RackSal(login, password, address, port, format)