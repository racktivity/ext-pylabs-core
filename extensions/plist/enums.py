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

class PFileType(pylabs.baseclasses.EnumerationWithValue):
    """
    Type of PFile
    
    @TODO: How to determine? Existing enum?
    """
    pass

PFileType.registerItem('UNKNOWN', 0)
PFileType.registerItem('FILE', 1)
PFileType.registerItem('DIRECTORY', 2)
PFileType.registerItem('BLOCK', 3)
PFileType.registerItem('CHAR', 4)
PFileType.registerItem('FIFO', 5)
PFileType.registerItem('SOCKET', 6)
PFileType.registerItem('LINK', 7)
PFileType.finishItemRegistration()




class PFileErrorCode(pylabs.baseclasses.EnumerationWithValue):
    """
    List of error codes of operations that can fail on a PFile
    """
    pass

PFileErrorCode.registerItem('NO_ERROR', 0)
PFileErrorCode.registerItem('COULD_NOT_LINK', 1)
PFileErrorCode.registerItem('COULD_NOT_SYMLINK', 2)
PFileErrorCode.registerItem('COULD_NOT_COPY', 3)
PFileErrorCode.registerItem('COULD_NOT_MOVE', 4)
PFileErrorCode.registerItem('COULD_NOT_DELETE', 5)
PFileErrorCode.registerItem('COULD_NOT_SET_SECURITY', 6)
PFileErrorCode.registerItem('COULD_NOT_SANDBOX', 7)
PFileErrorCode.finishItemRegistration()

class PFileFields(pylabs.baseclasses.EnumerationWithValue):
    """
    List of error codes of operations that can fail on a PFile
    """
    pass

PFileFields.registerItem('PROTECTIONMODE', 'protectionMode')
PFileFields.registerItem('INODENUMBER', 'inodeNumber')
PFileFields.registerItem('DEVICE', 'device')
PFileFields.registerItem('NUMBEROFLINKS', 'numberOfLinks')
PFileFields.registerItem('UID', 'uid')
PFileFields.registerItem('GID', 'gid')
PFileFields.registerItem('SIZE', 'size')
PFileFields.registerItem('ATIME', 'atime')
PFileFields.registerItem('MTIME', 'mtime')
PFileFields.registerItem('CTIME', 'ctime')
PFileFields.registerItem('MD5', 'md5')

#PFileFields.registerItem('ALL', 65535)
PFileFields.finishItemRegistration()