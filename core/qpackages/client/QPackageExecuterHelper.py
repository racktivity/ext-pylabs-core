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

from pymonkey import q, i
import sys
import random
import imp

class QPackageExecuterHelper(object):
    @staticmethod
    def executeMainMethodInScript(scriptFileLocation, argObject):
        """
        Execute the main method in a script
        @param scriptFileLocation: Location of the script to execute method in
        """
        if not q.system.fs.isFile(scriptFileLocation):
            raise IOError('Script %s does not exist'%scriptFileLocation)
        
        installerMain = QPackageExecuterHelper._getMethodFromModule(scriptFileLocation, 'main')
        
        result = installerMain(q, i, argObject)
        
        return result

    @staticmethod
    def _getMethodFromModule(modulePath, methodName):
        """
        Load a module and get a method
        @param modulePath: path of the module to load
        @param methodName: name of the method
        """
        modName = 'random'
        while modName in sys.modules:
            modName = 'qpackage_script_%d' % random.randint(0, sys.maxint)
    
        module = imp.load_source(modName, modulePath)
        method = getattr(module, methodName)
    
        return method