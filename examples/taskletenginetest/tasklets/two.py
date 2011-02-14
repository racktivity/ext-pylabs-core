__author__   = "someone"
__tags__     = "tag1",
__priority__ = 2

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    if params.has_key("tag3"):
        print "2 has tag tag1: param from 3: %s" % params["tag3"]
    else:
        print "2 has tag tag1"
    
