__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'removeAccount'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    accounts = [account for account in racktivity_application.accounts if account.login==params['login'] and str(account.accounttype)==params['accounttype']]
    
    if len(accounts) != 1:
        raise ValueError('The account specified could not be found!')
    
    racktivity_application.accounts.remove(accounts[0])
    q.drp.racktivity_application.save(racktivity_application)
    q.logger.log('Calling actor action to remove racktivity_application account', 3)
    #q.actions.actor.racktivity_application.removeAccount(racktivity_application.guid, account.guid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
