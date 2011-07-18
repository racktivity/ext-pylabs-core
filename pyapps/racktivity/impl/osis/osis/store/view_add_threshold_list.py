__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    columns = ('thresholdtype', 'thresholdimpacttype', 'tags')
    fields = dict()
    for column in columns:
        fields[column] = getattr(root, column)
    fields['cloudusergroupactions'] = ','.join(root.acl.cloudusergroupactions.keys()),
    osis.viewSave('threshold', 'view_threshold_list', root.guid, root.version, fields)
    q.logger.log('threshold rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'threshold'
