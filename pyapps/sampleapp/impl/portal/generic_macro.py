__tags__ = 'macro', 'generic'

def main(q, i, params, tags):
    params['result'] = 'Test of generic macro'

def match(q, i, params, tags):
    return True
