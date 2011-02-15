from pylabs import q
from pylabs.baseclasses.BaseEnumeration import EnumerationWithValue

from PgsqlAuth import PgsqlAuth
from BasicAuth import BasicAuth

class ApacheAuthType(EnumerationWithValue):
    """
    The type of (backend) authentication supported (see q.enumerators.ApacheAuthType)
    """
    pass


ApacheAuthType.registerItem("PGSQL",PgsqlAuth)
ApacheAuthType.registerItem("BASIC",BasicAuth)

ApacheAuthType.finishItemRegistration()
