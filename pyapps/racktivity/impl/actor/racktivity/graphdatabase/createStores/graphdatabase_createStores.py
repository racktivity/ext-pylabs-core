__author__ = 'racktivity'
__tags__ = 'graphdatabase', 'createStores'


def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    for storeid in params['storeids']:
        store.create(storeid)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True