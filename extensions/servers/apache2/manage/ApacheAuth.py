from ApacheSite import ApacheSite, SiteTemplate
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

class ApacheAuth(CMDBSubObject):
    """
    Authtentication Type
    """
    name = 'Authname'

    def __init__(self,name):
        CMDBSubObject.__init__(self)
        self.name = name
