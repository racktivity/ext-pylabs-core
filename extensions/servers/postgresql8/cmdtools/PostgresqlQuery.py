
import re
import time
import os

from pylabs import q
from pylabs.baseclasses.CommandWrapper import CommandWrapper
from pylabs.db.DBConnection import DBConnection

from pylabs.enumerators import AppStatusType

class PostgresqlQuery(CommandWrapper):

    _sqlcommand = "psql"
    
    def _executeSQL(self, username, sqlquery, database="postgres", options=""):

        cmd = '%(command)s --username=%(user)s %(options)s -c "%(query)s" %(db)s'%{'command': q.system.fs.joinPaths(os.sep, 'usr', 'lib', 'postgresql', '8.4', 'bin', self._sqlcommand),
                                                                                   'user'   : username,
                                                                                   'options': options,
                                                                                   'query'  : sqlquery,
                                                                                   'db'     : database,
                                                                                   }
        exitCode, output = q.system.process.execute(cmd, dieOnNonZeroExitCode=False)
        return output