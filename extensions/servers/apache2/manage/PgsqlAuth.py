from ApacheSite import ApacheSite, SiteTemplate
from ApacheAuth import ApacheAuth

class PgsqlAuth(ApacheAuth):
    """
    Class which does PostgreSQL backend authentication
    """
    host = 'localhost'
    port = '5432'
    user = None
    pwd = None
    database = None
    pwd_table = None
    uid_field = None
    pwd_field = None
    pwd_encrypted = 'off'


#    modules = {"auth_pgsql_module": "modules/mod_auth_pgsql.so"}

    def prepareConfig(self):
        """
        Return actual configuration values
        """
        items = list()

        items.append("Auth_PG_host %s" % self.host)
        items.append("Auth_PG_port %s" % self.port)
        items.append("Auth_PG_user %s" % self.user)
        items.append("Auth_PG_pwd %s" % self.pwd)
        items.append("Auth_PG_database %s" % self.database)
        items.append("Auth_PG_pwd_table %s" % self.pwd_table)
        items.append("Auth_PG_uid_field %s" % self.uid_field)
        items.append("Auth_PG_pwd_field %s" % self.pwd_field)
        items.append("Auth_PG_encrypted %s" % self.pwd_encrypted)

        return items
