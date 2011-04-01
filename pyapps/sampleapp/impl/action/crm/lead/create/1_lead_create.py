__author__ = 'incubaid'

def main(q, i, p, params, tags):
    lead = p.api.model.crm.lead.new()
    lead.name = params['name']
    lead.code = params['code']
    lead.customerguid = params['customerguid']
    lead.source = params['source']
    lead.type = params.get('type')
    lead.status = params.get('status')
    lead.amount = params.get('amount')
    lead.probability = params.get('probability')    
    p.api.model.crm.lead.save(lead)
    params['result'] = lead.guid
    
def match(q, i, p, params, tags):
	return True