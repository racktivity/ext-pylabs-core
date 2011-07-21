__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    import time
    result = [0,0,0]
    currenttime = int(time.time())
    timing = params["timing"]
    
    md = p.api.model.racktivity.meteringdevice.get(params["guid"])
    lastaccessed = md.lastaccessed
    if lastaccessed > (currenttime - timing[0]):
        result[0] += 1
    elif lastaccessed > (currenttime - timing[1]):
        result[1] += 1
    else:
        result[2] += 1
    params['result'] = {"returncode":True, "healthstatus":result}

def match(q, i, params, tags):
    return True
