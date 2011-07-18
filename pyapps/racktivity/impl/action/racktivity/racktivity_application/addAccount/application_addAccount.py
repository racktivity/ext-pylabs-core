__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'addAccount'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Adding racktivity_application account to model', 3)
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    account = racktivity_application.accounts.new()
    account.login = params['login']
    account.passwd = params['password']
    account.accounttype = params['accounttype']
    racktivity_application.accounts.append(account)
    q.drp.racktivity_application.save(racktivity_application)
    q.logger.log('Calling actor action to provision racktivity_application account', 3)
    q.actions.actor.racktivity_application.addAccount(racktivity_application.guid, account.guid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
