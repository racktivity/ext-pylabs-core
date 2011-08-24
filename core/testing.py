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

import os
import os.path
import unittest
import tempfile
import shutil

class pylabsTestCase(unittest.TestCase):
    def setUp(self):
        from pylabs import q
        if not q._init_called:
            from pylabs.InitBase import q

from pylabs.enumerators import PlatformType

class DisabledTestCase(unittest.TestCase):
    def run(self, *args, **kwargs):
        print 'Testcase is disabled'
        return

def PlatformSpecificTestCase(platform, *args, **kwargs):
    '''Return class_ if platform is current platform, otherwise return object

    This can be used to create TestCase classes which should only be executed
    on one or more specific platforms, eg:

    >>> class MyTest(PlatformSpecificTestCase(PlatformType.LINUX)):
    ...     def test_foo(self):
    ...         self.assert_(True)

    This test will only work on Linux systems.

    @param platform: Platform or list of platforms
    @type platform: PlatformType
    @param args: List of extra supported platforms
    @type args: list<PlatformType>
    @param kwargs.class_: Type to return if platform matches
    @type kwargs.class_: type

    @returns: Requested class on platform match, or C{DisabledTestCase}
    @rtype: type
    '''
    class_ = kwargs.get('class_', unittest.TestCase)
    local_platform = PlatformType.findPlatformType()
    if isinstance(platform, PlatformType):
        platforms = (platform, )
    else:
        platforms = tuple(platform)

    for platform in platforms:
        if local_platform.has_parent(platform):
            return class_

    return DisabledTestCase
