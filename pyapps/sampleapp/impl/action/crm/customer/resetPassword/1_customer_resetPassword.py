__author__ = 'incubaid'

def main(q, i, p, params, tags):
    
    customer = p.api.model.crm.customer.get(params['customerguid'])
    customer.password = params['password']

    p.api.model.crm.customer.save(customer)
    message = """
Dear %s,

Your password has been reset. Your new password is : %s

Regards,

The Incubaid team.
    """ %(customer.name, customer.password)
    p.api.actor.crm.mailprocessor.sendMail(sender='crm@incubaid.com', replyto='crm@incubaid.com', to=customer.email, subject='Password Reset', message=message)['result']
    params['result'] = customer.guid
    
def match(q, i, p, params, tags):
	return True
