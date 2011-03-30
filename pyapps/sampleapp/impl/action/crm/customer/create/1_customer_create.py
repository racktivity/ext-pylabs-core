__author__ = 'incubaid'

def main(q, i, p, params, tags):
    customer = p.api.model.crm.customer.new()
    customer.name = params['name']
    customer.email = params['email']
    customer.login = params['login']
    customer.password = params['password']
    customer.address = params.get('address')
    customer.vat = params.get('vat')
    p.api.model.crm.customer.save(customer)
    message = """
    Dear %(name)s,
    
    Welcome to the Incubaid CRM system!
    
    Regards,
    
    The Incubaid team.
    """
    params['result'] = p.api.actor.crm.mailprocessor.sendMail(sender='crm@incubaid.com', replyto='crm@incubaid.com', to=customer.email, 
                                                              subject='Welcome!', message=message%{"name": customer.name})['result']
    
def match(q, i, p, params, tags):
	return True