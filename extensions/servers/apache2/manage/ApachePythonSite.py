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
 
from pymonkey import q

from ApacheSite import ApacheSite, SiteTemplate

PythonSiteTemplate = SiteTemplate.subclass(source="""
    #implements SiteTemplate.respond
    #block directory_start
        SetHandler mod_python
        PythonPath "$pythonPath"
        PythonHandler $pythonHandler
        #for $option in $pythonOptions
            PythonOption $option
        #end for
        #if $pythonDebug
            PythonDebug On
        #else
            PythonDebug Off
        #end if
        AddHandler mod_python .py
    #end block
""")

class ApachePythonSite(ApacheSite):
    """
    Class which is responsible for the configuration of 1 Apache Python site
    """
    pythonDebug = q.basetype.boolean(doc="enable python debugging", default=False)
    pythonHandler = q.basetype.string(doc="python handler", default="mod_python.publisher")
    pythonPath = q.basetype.string(doc="python path", default="sys.path")
    pythonOptions = q.basetype.list(doc="python options")

    pm_template = PythonSiteTemplate

    modules = {"python_module": "modules/mod_python.so"}

    def pm_getTemplateContext(self, aclFileDir):
        parentContext = ApacheSite.pm_getTemplateContext(self, aclFileDir)
        parentContext.update({
            "pythonPath": self.pythonPath,
            "pythonHandler": self.pythonHandler,
            "pythonDebug": self.pythonDebug,
            "pythonOptions": self.pythonOptions,
        })
        return parentContext