
def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    params['result'] = osis.objectsFindAsView(params['domain'],
        params['rootobjecttype'],
        params['filterobject'],
        params['osisview'])
