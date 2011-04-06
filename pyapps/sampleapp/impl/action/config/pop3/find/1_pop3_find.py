__author__ = 'incubaid'

def main(q, i, p, params, tags):
    filterObject = p.api.config.mail.pop3.getFilterObject()

    fields = ('server','login')
    for key,value in params.iteritems():
        if key in fields and not value in (None, ''):
            filterObject.add('config_view_pop3_list', key, value)
          
    result = p.api.config.mail.pop3.find(filterObject)
    params['result'] = result

    
def match(q, i, p, params, tags):
	return True
