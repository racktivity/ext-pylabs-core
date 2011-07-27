__author__ = 'racktivity'

def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    value = store.getLatest(params['storeid'])
    params['result'] = {'returncode': True, 'value': value}

def match(q, i, params, tags):
    return True
