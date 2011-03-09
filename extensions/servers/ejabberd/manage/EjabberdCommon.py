from pylabs import q

def setRestartRequired(self, value):
    q.manage.ejabberd.cmdb.dirtyProperties.add('restartRequired')
    yield value