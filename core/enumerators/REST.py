from pylabs.baseclasses import BaseEnumeration

class RESTResultFormat(BaseEnumeration):
    """
    Enumerator of all supported Bitbucket REST result formats
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('json')
        cls.registerItem('yaml')
        cls.registerItem('xml')
        cls.finishItemRegistration()

class RESTMethod(BaseEnumeration):
    """
    Enumerator of all supported REST methods
    """

    @classmethod
    def _initItems(cls):
        cls.registerItem('POST')
        cls.registerItem('GET')
        cls.registerItem('PUT')
        cls.registerItem('DELETE')
        cls.finishItemRegistration()
