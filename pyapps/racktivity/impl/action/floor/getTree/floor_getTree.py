__author__ = 'aserver'
__tags__ = 'floor', 'getTree'
__priority__= 3

def main(q, i, params, tags):
    from rootobjectaction_lib import rootobject_tree
    params['result'] = {"returncode":True, "tree":rootobject_tree.getTree(params["floorguid"], params["depth"])}

def match(q, i, params, tags):
    return True


