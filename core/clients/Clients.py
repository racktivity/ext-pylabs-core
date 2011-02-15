
from pylabs.enumerators import PlatformType
from pylabs.decorators import deprecated

class Clients(object):
    ssh = None

    def __getattribute__(self, name):
        try:
            tool = object.__getattribute__(self, name)
            if tool:
                return tool
        except AttributeError:
            pass
        
        def ssh():
            from pylabs.clients.ssh.SSHTool import SSHTool
            return SSHTool()

        if name in locals():
            tool = locals()[name]()
            setattr(self, name, tool)
            return tool

        raise AttributeError
