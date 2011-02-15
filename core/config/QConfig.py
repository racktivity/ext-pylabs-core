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

import pylabs

class QConfig():
    """
    pylabs singleton class available under q.config
    Meant for non interactive access to configuration items
    """
    def getInifile(self, configtype):
        fileAlreadyExists = pylabs.q.system.fs.exists(self._buildPath(configtype))
        return pylabs.inifile.IniFile(self._buildPath(configtype), create=(not fileAlreadyExists))
    
    def getConfig(self, configtype):
        """
        Return dict of dicts for this configuration.
        E.g. { 'pylabs.org'    : {url:'http://pylabs.org', login='test'} ,
               'trac.qlayer.com' : {url:'http://trac.qlayer.com', login='mylogin'} }
        """
        ini = self.getInifile(configtype)
        return ini.getFileAsDict()
    
    def remove(self, configtype):
        pylabs.q.system.fs.removeFile(self._buildPath(configtype))
        
    def list(self):
        """
        List all configuration types available.
        """
        qconfigPath = pylabs.q.system.fs.joinPaths(pylabs.q.dirs.cfgDir, "qconfig")
        if not pylabs.q.system.fs.exists(qconfigPath):
            return []
        fullpaths = pylabs.q.system.fs.listFilesInDir(qconfigPath)
        return [pylabs.q.system.fs.getBaseName(path)[:-4] for path in fullpaths if path.endswith(".cfg")]

    def _buildPath(self, configtype):
        return pylabs.q.system.fs.joinPaths(pylabs.q.dirs.cfgDir, "qconfig", configtype + ".cfg")