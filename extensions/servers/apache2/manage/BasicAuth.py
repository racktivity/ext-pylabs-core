from ApacheSite import ApacheSite, SiteTemplate
from ApacheAuth import ApacheAuth

class BasicAuth(ApacheAuth):
    """
    Empty Auth class
    """

#    modules = {"auth_pgsql_module": "modules/mod_auth_pgsql.so"}

    def prepareConfig(self):
        """
        Return actual configuration values
        """
        items = list()
        return items
