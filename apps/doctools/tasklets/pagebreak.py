__tags__ = ("macro", "pagebreak")
__author__ = 'Incubaid'

def match(q, i, params, tags):
    print tags
    return True

def main(q, i, params, tags):
    params['result'] = "{tokenized}\nPB||\n{tokenized}"
    return True
