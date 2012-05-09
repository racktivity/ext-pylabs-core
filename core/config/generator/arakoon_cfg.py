from pylabs import q
join = q.system.fs.joinPaths

class ArakoonPyApps:

    def __init__(self, appName, user=None, group=None):
        self.appName = appName

        # username and group used for running arakoon
        self.user = user
        self.group = group

    def generate_cfg(self, baseport):
        config = q.clients.arakoon.getClientConfig(self.appName)
        if config.getNodes():
            return
        baseport = int(baseport)
        s = q.manage.arakoon.getCluster(self.appName)
        if not s.listNodes():
            s.setUp(1, baseport, user=self.user, group=self.group)
        config = q.clients.arakoon.getClientConfig(self.appName)
        if not config.getNodes():
            config.generateFromServerConfig()
