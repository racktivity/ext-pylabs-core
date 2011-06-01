__author__ = "Incubaid"

FIELDS = []
FIELDS.append("password")
FIELDS.append("name")
FIELDS.append("groups")

TYPE = "user"
GUID_FIELD = "%sguid" % TYPE
DOMAIN = "crm"
VIEW = "%s_view_%s_list" % (DOMAIN, TYPE)

def get_model_handle(p):
    return p.api.model.crm.user

def main(q, i, p, params, tags):
    handle = get_model_handle(p)
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
