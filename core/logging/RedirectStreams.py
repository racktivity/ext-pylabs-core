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

import sys
import pylabs

original_stdout = None
original_stderr = None

class _Redirector:

    def __init__(self, stream, hideoutput, loglevel):
        self.loglevel = loglevel
        self.savedstream = stream
        self.hideoutput = hideoutput
        self.stringBuff = ''
 
    def write(self, string):
        if not self.hideoutput:
            self.savedstream.write(string)
        if pylabs.q.logger.inlog==False:
            if self.stringBuff <> '':
                pylabs.q.logger.log(self.stringBuff, self.loglevel,dontprint=True)
                self.stringBuff=''
            pylabs.q.logger.log(string, self.loglevel,dontprint=True)

    def flush(self):
        self.savedstream.flush()
        
    def writelines(self,lines):
        for line in lines:
            self.write(line)
            
    def fileno(self):
        return self.savedstream.fileno()

def isRedirected(stream):
    return isinstance(stream, _Redirector)


def redirectStreams(hideoutput=False, loglevel=4, stdout=True, stderr=True):
    """
    Redirect sys.stdout and sys.stderr to q.logger.
    Original streams are saved as original_stdout and original_stderr in this package
    @hideoutput: boolean indicating whether output must still be sent to original stderr/stdout
    @loglevel: log severity level to be used
    @stdout: boolean indicating whether sys.stdout must be redirected
    @stderr: boolean indicating whether sys.stderr must be redirected
    """
    
    if stdout:
        sys._stdout_ori = sys.stdout
        sys.stdout = _Redirector(sys.stdout, hideoutput, loglevel)
    
    if stderr:
        sys._stderr_ori = sys.stderr
        sys.stderr = _Redirector(sys.stdout, hideoutput, loglevel)