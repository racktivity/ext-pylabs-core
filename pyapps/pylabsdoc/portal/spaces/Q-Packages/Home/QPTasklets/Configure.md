@metadata title=Configure Tasklet

[[code]]
__author__ = 'incubaid'
__tags__   = 'configure',

def main(q, i, params, tags):
    qpackage = params['qpackage']
    url = 'http://127.0.0.1/pylabsdoc/'
    q.manage.nginx.startChanges()
    vhost = q.manage.nginx.cmdb.virtualHosts['80']
    if vhost:
        if '/'in vhost.reverseproxies:
            q.logger.log('reverse proxy already configured', level=3)
        else:
	        vhost.addReverseProxy('/', url, '/')
	        q.manage.nginx.save()
	        q.mange.nginx.applyConfig()
    else:
        q.logger.log('No virtualHost 80 exists!', level=3)
[[/code]]