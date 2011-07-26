__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Adding application account to model', 3)
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    account = application.accounts.new()
    account.login = params['login']
    account.passwd = params['password']
    account.accounttype = params['accounttype']
    application.accounts.append(account)
    p.api.model.racktivity.application.save(application)
    q.logger.log('Calling actor action to provision application account', 3)
    p.api.actor.application.addAccount(application.guid, account.guid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
