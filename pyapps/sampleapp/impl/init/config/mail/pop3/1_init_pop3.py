def main (q, i, p, params, tags):
    connection = p.application.getAPI(params['appname']).action
    # TODO - MNOUR: The domain should not be config. This will be solved in another bug.
    q.logger.log("[INIT-POP3] - Creating a POP3 mail box '%s' on '%s' server" %('analytics@incubaid.com', 'pop.gmail.com'), level=3)
    #connection.config.pop3.create('pop.gmail.com', 'analytics@incubaid.com', 'somepasswd')
    params['result'] = True
