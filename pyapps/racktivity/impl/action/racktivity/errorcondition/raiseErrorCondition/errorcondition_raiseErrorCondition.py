__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    level = params['level']
    if not level:
        level = 'WARNING'
    #Overwrite default application settings
    q.application.appname = 'cloudapi'
    q.application.agentid = q.agentid

    try:
        handler = getattr(q.errorconditionhandler, 'raise%s' % level.capitalize())
        handler(fields['publicmessage'], fields['privatemessage'], fields['typeid'], fields['tags'], True)
    except:
        #Catch exception if raiseError / raiseCritical is used
        pass
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
