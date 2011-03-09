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
from pylabs.baseclasses.CommandWrapper import CommandWrapper

class ApachePasswdCommand(CommandWrapper):
    """
    The Apache htpasswd commandWrapper to update passwords
    """
    def _getHtpasswdBinary(self):
        return q.system.fs.joinPaths(os.sep, "usr", "bin", "htpasswd")
            
    def createACE(self, accessFilePath, userName, passwd, createPwdFile):
        """
        Adds an ACE to the apache configuration
                @param accessFilePath : path of the ACL file
                @param userName :  the username to add
                @param passwd : the password that will be set for the username
                @param createPwdFile : boolean indicating if the passwdfile has to be created.  If passwdfile already exists, it is rewritten and truncated
        """
        create = ""
        if createPwdFile == True:
            create = "c"
            
        try:
            command = "%(htpasswd)s -b%(create)s %(accessFilePath)s %(userName)s '%(passwd)s'"%{"htpasswd":self._getHtpasswdBinary(), "accessFilePath":accessFilePath, "userName":userName, "passwd":passwd, "create":create}
            exitCode, output = q.system.process.execute(command)
        except Exception, e:
            raise RuntimeError, "Access control entry could not be created", e