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
if not sys.platform.startswith('win'):
    raise "WinRegHiveType enumerator is only supported on Windows operating system"

from pylabs.baseclasses import BaseEnumeration
import _winreg as reg

class WinRegHiveType(BaseEnumeration):
    ''' The windows registry hive, or section '''

    def __init__(self, hive):
        self.hive = hive

    def __repr__(self):
        return str(self)

    
WinRegHiveType.registerItem('hkey_classes_root', reg.HKEY_CLASSES_ROOT)
WinRegHiveType.registerItem('hkey_current_user', reg.HKEY_CURRENT_USER)
WinRegHiveType.registerItem('hkey_local_machine', reg.HKEY_LOCAL_MACHINE)
WinRegHiveType.registerItem('hkey_users', reg.HKEY_USERS)
WinRegHiveType.registerItem('hkey_current_config', reg.HKEY_CURRENT_CONFIG)
WinRegHiveType.finishItemRegistration()