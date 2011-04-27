__author__ = 'incubaid'

def main(q, i, p, params, tags):
    pop3 = p.api.config.mail.pop3.new()
    pop3.server = params['server']
    pop3.login = params['login']
    pop3.password = params['password']
    p.api.config.mail.pop3.save(pop3)
    params['result'] = True
    
def match(q, i, p, params, tags):
	return True
