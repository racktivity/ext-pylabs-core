__tags__ = "test", "setup"
__author__ = "racktivity"
__priority__ = 90

def main(q, i, params, tags):
    q.qp.findNewest('racktivity_framework').install()

def match(q, i, params, tags):
    return params['stage'] == 1