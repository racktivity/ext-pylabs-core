# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>

from pylabs import q
from pylabs.baseclasses import BaseType
from pylabs.enumerators import PlatformType
from pylabs.qpackages.common.enumerators import DependencyType

class DependencyDef(BaseType):
 
    name=q.basetype.string(doc="official name of qpackage, is part of unique identifier of qpackage")
    minversion=q.basetype.string(doc="Version of qpackage normally x.x format, is part of unique identifier of qpackage", allow_none=True)
    maxversion=q.basetype.string(doc="Version of qpackage normally x.x format, is part of unique identifier of qpackage", allow_none=True)
    domain=q.basetype.string(doc="url of domain, is part of unique identifier of qpackage")
    supportedPlatforms=q.basetype.list(doc="supported platforms, see q.enumerators.platformtypes.")
    dependencyType= q.basetype.enumeration(DependencyType, doc='Type of the Dependency', default=DependencyType.RUNTIME)

    def __str__(self):
        return "%s %s %s" % (self.domain, self.name, self.dependencyType)

    def __repr__(self):
        return self.__str__()