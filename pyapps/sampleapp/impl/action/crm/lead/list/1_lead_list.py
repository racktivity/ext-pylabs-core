__author__ = "Incubaid"

FIELDS = (
        'name',
        'code',
        'customerguid',
        'soure',
        'type',
        'status',
        'amount',
        'probability'
        )

TYPE = "lead"
DOMAIN = "crm"
JOBGUID = "jobguid"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def to_dict(o):
    return dict((field, getattr(o, field)) for field in FIELDS)

def get_model_handle(p):
    return p.api.model.crm.lead

def main(q, i, p, params, tags):
    handle = get_model_handle(p)

    if JOBGUID not in params:
        raise ValueError("Cannot delete %s, there is no %s key in the params" % (TYPE, JOBGUID))
    jobguid = params[JOBGUID]

    f = handle.getFilterObject()
    f.add(VIEW, "jobguid", jobguid)
    objects = handle.filter(f)

    result = [to_dict(o) for o in objects]
    params['result'] = result
