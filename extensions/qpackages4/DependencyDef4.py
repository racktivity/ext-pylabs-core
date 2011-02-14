from pymonkey import q
from pymonkey.baseclasses import BaseType
from enumerators4 import DependencyType4

class DependencyDef4(BaseType):
 
    name=q.basetype.string(doc="official name of qpackage, is part of unique identifier of qpackage")
    minversion=q.basetype.string(doc="Version of qpackage normally x.x format, is part of unique identifier of qpackage", allow_none=True)
    maxversion=q.basetype.string(doc="Version of qpackage normally x.x format, is part of unique identifier of qpackage", allow_none=True)
    domain=q.basetype.string(doc="url of domain, is part of unique identifier of qpackage")
    supportedPlatforms=q.basetype.list(doc="supported platforms, see q.enumerators.PlatformType.")
    dependencytype= q.basetype.enumeration(DependencyType4, doc='Type of the Dependency', default=DependencyType4.RUNTIME)

    def __str__(self):
        return "%s_%s %s-%s %s for platforms: %s" % (self.domain, self.name, self.minversion, self.maxversion, self.dependencytype, str(self.supportedPlatforms))

    def __repr__(self):
        return self.__str__()