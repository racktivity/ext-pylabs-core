__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    import commands
    destDir = params["destinationdir"]
    stat, out = commands.getstatusoutput("backup.sh '%s'"%destDir)
    if stat:
        raise Exception("Backup operation failed:\n%s"%out)
    #Get the file name
    outlines = out.strip().split("\n")
    params['result'] = {'returncode': True, "filename":outlines[len(outlines) - 1]}

def match(q, i, params, tags):
    return True
