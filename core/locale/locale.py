import os
import re
from pylabs import q
KEYP = re.compile("(\w+(\.\w+)*)\s*=\s*(.*)", re.DOTALL)

DEFAULTLOCALE='en'

class Domain(dict):
    def __init__(self, key):
        self.value = None
        self.__key = key
    
    @property
    def key(self):
        return self.__key
    
    def __getattr__(self, attr):
        if attr in self:
            domain = self[attr]
        else:
            domain = Domain("%s.%s" % (self.key, attr))
            self[attr] = domain
            
        return domain
    
    def __call__(self, **args):
        return str(self) % args
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return str(self.value) if self.value != None else self.key

class Localizer(object):
    def __init__(self, tdirs):
        self.__domains = self.__load(tdirs)
    
    def __load(self, tdirs):
        domains = {}
        for path in q.system.fs.listFilesInDir(tdirs, filter="*.l"):
            locale = os.path.splitext(q.system.fs.getBaseName(path))[0]
            domain = Domain(locale)
            with open(path) as f:
                l = 0
                for line in f:
                    l += 1
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    m = re.match(KEYP, line)
                    if not m:
                        raise RuntimeException("Invalid line at '%s:%d'" % (path, l))
                    k = m.group(1)
                    v = m.group(3)
                    
                    d = domain
                    for kp in k.split("."):
                        d = getattr(d, kp)
                    d.value = v
            domains[locale] = domain
        
        return domains
    
    def __call__(self, locale):
        if locale in self.__domains:
            return self.__domains[locale]
        elif DEFAULTLOCALE in self.__domains:
            return self.__domains[DEFAULTLOCALE]
        else:
            raise RuntimeError("Can't find locale '%s' or the default '%s' locale" % (locale, DEFAULTLOCALE))