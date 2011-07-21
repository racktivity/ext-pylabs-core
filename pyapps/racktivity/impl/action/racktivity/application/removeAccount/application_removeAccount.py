__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    accounts = [account for account in application.accounts if account.login==params['login'] and str(account.accounttype)==params['accounttype']]
    
    if len(accounts) != 1:
        raise ValueError('The account specified could not be found!')
    
    application.accounts.remove(accounts[0])
    p.api.model.racktivity.application.save(application)
    q.logger.log('Calling actor action to remove application account', 3)
    #q.actions.actor.application.removeAccount(application.guid, account.guid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
