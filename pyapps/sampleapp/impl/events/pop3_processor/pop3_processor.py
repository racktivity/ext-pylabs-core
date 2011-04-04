def main(q, i, p, params, tags):
    p.api.action.crm.lead.create('test', 'test', 'CBAC660B-BFEC-48AE-A619-620ECF27038D', 'COLDCALL', 'NEWBUSINESS', 'PROSPECTING')

def match(q, i, params, tags):
    import base64
    tags = q.base.tags.getObject( params["eventBody"] )
    return '!@***LEAD***@!' in base64.decodestring(tags.tagGet("mail"))
