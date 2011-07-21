__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getThresholdOnPowerPort'

def main(q, i, params, tags):
    raise NotImplementedError()

def match(q, i, params, tags):
    return params['devicetype'] == "apc"

