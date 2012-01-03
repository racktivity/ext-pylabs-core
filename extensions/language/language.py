from pylabs import q, p
import re, os
import json

KEYP = re.compile("(\w+(\.\w+)*)\s*=\s*(.*)", re.DOTALL)

class JSLanguageCompiler(object):
    def compile(self, appname):
        
        outpath = q.system.fs.joinPaths(q.dirs.pyAppsDir,
                                     appname, 'portal', 'static', 'js', 'lang')
        
        lpath = q.system.fs.joinPaths(outpath, 'src')
        if not q.system.fs.isDir(lpath):
            return
        
        for lfile in q.system.fs.listFilesInDir(lpath, filter="*.l"):
            package = os.path.splitext(q.system.fs.getBaseName(lfile))[0]
            domain = {}
            with open(lfile) as file:
                l = 0
                append = False
                lastdomain = domain
                for line in file:
                    l += 1
                    line = line.strip()
                    if not line or line.startswith("#"):
                        append=False
                        continue
                    if append:
                        lastdomain['value'] += "\n" + line.rstrip("\\")
                        if not line.endswith("\\"):
                            append=False
                        continue
                    
                    append = line.endswith("\\")
                    line = line.rstrip("\\")
                    m = re.match(KEYP, line)
                    if not m:
                        raise RuntimeError("Invalid line at '%s:%d'" % (lfile, l))
                    k = m.group(1)
                    v = m.group(3)
                    
                    d = domain
                    for kp in k.split("."):
                        if 'sub' not in d:
                            d['sub'] = {}
                        d = d['sub']
                        if kp not in d:
                            d[kp] = {}
                        d = d[kp]
                    
                    d['value'] = v
                    lastdomain = d
            q.system.fs.writeFile(q.system.fs.joinPaths(outpath, "%s.json" % package),
                                  json.dumps(domain))
            
