import base64

FIELDS = (
          'name',
          'code',
          'customerguid',
          'source',
          'type',
          'status',
          'amount',
          'probability'
          )

def main(q, i, p, params, tags):
    # Parse the lead information from the event body parameter
    q.logger.log('[DEBUG] - In pop3_processor:main', level=3)
    decodedparams = base64.decodestring(q.base.tags.getObject(params['eventBody']).tagGet('mail'))
    q.logger.log('[DEBUG] - Decoded params are: %s' %decodedparams,  level=3)
    parameters = dict()
    for line in decodedparams.splitlines():
        if line and line !=  '!@***LEAD***@!':
            param = line.split('=')
            if len(param) == 2:
                parameters[param[0].strip()] = param[1].strip()
    for field in FIELDS:
        parameters[field] = parameters.get(field)

    q.logger.log('[DEBUG] - parameters are: %s' %str(parameters), level=3)
    if not parameters.get('name') or not parameters.get('code'):
        q.errorconditionhandler.raiseError("Can not create a new Lead with these missing fields: 'name' and 'code'.")

    p.api.action.crm.lead.create(parameters['name'], parameters['code'], customerguid=parameters['customerguid'],
                                 source=parameters['source'], type=parameters['type'], status=parameters['status'],
                                 amount=parameters['amount'], probability=parameters['probability'])

    params['result'] = True

def match(q, i, params, tags):
    q.logger.log('[DEBUG] - In pop3_processor:match', level=3)
    q.logger.log('[DEBUG] - Event body: %s' %params['eventBody'], level=3)
    tags = q.base.tags.getObject(params['eventBody'])
    q.logger.log('[DEBUG] - Decoded new Lead information: %s' %base64.decodestring(tags.tagGet('mail')), level=3)
    return '!@***LEAD***@!' in base64.decodestring(tags.tagGet('mail'))
