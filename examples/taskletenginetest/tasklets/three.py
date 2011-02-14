__author__   = "someone"
__tags__     = "tag3",
__priority__ = 3

def match(q, i, params, tags):
    return True

def main(q, i, params, tags):
    print "3 has tag tag3"
    params["tag3"]="three inserted this paramvalue"
    
    
