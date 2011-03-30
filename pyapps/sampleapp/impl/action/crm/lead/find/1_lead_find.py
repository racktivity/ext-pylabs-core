__author__ = "Incubaid"

FIELDS = (
        'name',
        'code',
        'customerguid',
        'source',
        'type',
        'status',
        'amount',
        'probability',
        'jobguid'
        )
TYPE = "lead"
GUID_FIELD = "%sguid" % TYPE
DOMAIN = "crm"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def get_model_handle(p):
    return p.api.model.crm.lead

def main(q, i, p, params, tags):
    handle = get_model_handle()
    f = handle.getFilterObject()

    for field in FIELDS:
        if field not in params:
            q.logger.log("Field %s not in params dict: not searching for field %s" % (field, field), 7)
            continue

        value = params[field]
        if value is None:
            q.logger.log("Field %s is None: not searching for field %s" % (field, field), 7)
            continue

        q.logger.log("Adding filter on field %s with value value %s" % (field, value), 7)
        f.add(VIEW, field, value)

    result = handle.find(f)
    params['result'] = result
