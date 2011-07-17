__author__ = 'aserver'
__tags__ = 'racktivity', 'findObjects'
__priority__= 3

def main(q, i, params, tags):
    from rootobjectaction_lib import rootobject_search
    result = rootobject_search.search(params["searchstring"])
    maxresults = params["maxresults"]
    index = params["index"]
    if maxresults: 
        params["result"] = result[index:index + maxresults]
    else:
        params["result"] = result[index:]

def match(q, i, params, tags):
    return True
