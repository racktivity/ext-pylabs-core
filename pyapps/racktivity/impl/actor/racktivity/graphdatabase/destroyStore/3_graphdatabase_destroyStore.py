__author__ = 'racktivity'


def main(q, i, params, tags):
    import storelib
    store = storelib.cfgfactory()
    storeid = params['storeid']
    if store.exists(storeid):
        store.destroy(storeid)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True