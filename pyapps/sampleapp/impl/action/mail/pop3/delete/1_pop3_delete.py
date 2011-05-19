__author__ = 'incubaid'

def main(q, i, p, params, tags):
    
    p.api.model.mail.pop3.delete(params['pop3guid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
    return True
