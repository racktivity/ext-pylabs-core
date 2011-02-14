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

__all__ = ['BaseDescriptor', ]

__all__ += ['Boolean', 'Integer', 'Float', 'String', ]

__all__ += ['Guid', ]
__all__ += ['Path', 'DirPath', 'FilePath', ]
__all__ += ['UnixDirPath', 'UnixFilePath', ]
__all__ += ['WindowsDirPath', 'WindowsFilePath', ]
__all__ += ['IPv4Address', ]

from pymonkey.properties.common import BaseDescriptor

from pymonkey.properties.primitives import Boolean, Integer, Float, String

from pymonkey.properties.collections import Dictionary, List, Set

from pymonkey.properties.customtypes import Guid
from pymonkey.properties.customtypes import Path, DirPath, FilePath
from pymonkey.properties.customtypes import UnixDirPath, UnixFilePath
from pymonkey.properties.customtypes import WindowsDirPath, WindowsFilePath
from pymonkey.properties.customtypes import IPv4Address