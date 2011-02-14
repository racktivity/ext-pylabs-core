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

'''Definition of several custom types (paths, ipaddress, guid,...)'''

import re

from pymonkey.pmtypes import PrimitiveTypes
from pymonkey.pmtypes.base import BaseType
from pymonkey.pmtypes import IPv4Range, IPv4Address
GUID_RE = re.compile('^[0-9a-fA-F]{8}[-:][0-9a-fA-F]{4}[-:][0-9a-fA-F]{4}[-:][0-9a-fA-F]{4}[-:][0-9a-fA-F]{12}$')
class Guid(PrimitiveTypes.String):
    '''Generic GUID type'''
    NAME = 'guid'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid GUID string'''
        if not PrimitiveTypes.String.check(value):
            return False
        return GUID_RE.match(value) is not None

class Path(PrimitiveTypes.String):
    '''Generic path type'''
    NAME = 'path'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid path

        This checks whether value is a valid string only.
        '''
        return PrimitiveTypes.String.check(value)

class DirPath(Path):
    '''Generic folder path type'''
    NAME = 'dirpath'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid directory path

        This checks whether value is a valid Path only.
        '''
        return Path.check(value)

class FilePath(Path):
    '''Generic file path type'''
    NAME = 'filepath'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid file path

        This checks whether value is a valid Path only.
        '''
        return Path.check(value)

class UnixDirPath(DirPath):
    '''Generic Unix folder path type'''
    NAME = 'unixdirpath'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid UNIX directory path

        This checks whether value is a valid DirPath which starts and stops
        with '/'.
        '''
        if not DirPath.check(value):
            return False
        return value.startswith("/") and value.endswith("/")

class UnixFilePath(FilePath):
    '''Generic Unix file path type'''
    NAME = 'unixfilepath'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid UNIX file path

        This checks whether value is a valid FilePath which starts with '/' and
        does not end with '/'.
        '''
        if not FilePath.check(value):
            return False
        return value.startswith("/") and not value.endswith("/")

WINDOWS_DIR_RE = re.compile('^([a-zA-Z]:)?[\\\\/]')
class WindowsDirPath(DirPath):
    '''Generic Windows folder path type'''
    NAME = 'windowsdirpath'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid Windows directory path

        This checks whether value is a valid DirPath which starts with '/' or
        '\\', optionally prepended with a drive name, and ends with '/' or
        '\\'.
        '''
        if not DirPath.check(value):
            return False

        if not WINDOWS_DIR_RE.match(value):
            return False
        return value.endswith(('\\', '/', ))

WINDOWS_FILE_RE = re.compile('^([a-zA-Z]:)?[\\\\/]')
class WindowsFilePath(FilePath):
    '''Generic Windows file path type'''
    NAME = 'windowsfilepath'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid Windows file path

        This checks whether value is a valid FilePath which starts with '/' or
        '\\', optionally prepended with a drive name, and not ends with '/' or
        '\\'.
        '''
        if not FilePath.check(value):
            return False

        if not WINDOWS_FILE_RE.match(value):
            return False
        return not value.endswith(('\\', '/', ))


class IPAddress(PrimitiveTypes.String):
    '''Generic IPv4 address type'''
    NAME = 'ipaddress'

    @staticmethod
    def check(value):
        '''Check whether provided value is a valid IPv4 address

        @param value: IP address to check
        @type value: string

        @returns: Whether the provided value is a valid IPv4 address
        @rtype: bool
        '''
        items = str(value).split('.')
        if len(items) != 4:
            return False
        try:
            items = [x for x in items if int(x) > -1 and int(x) < 256]
        except ValueError:
            return False
        return len(items) == 4

class IPv4AddressRange(BaseType):
    '''Generic IPv4 address range type'''
    NAME = 'ipaddressrange'

    @staticmethod
    def check(value):
        '''
        Check if the value is a valid IPv4AddressRange
        We just check if the value is a instance of a IPv4Range
        '''
        return isinstance(value,IPv4Range)

class IPPort(BaseType):
    '''Generic IP port type'''
    NAME = 'ipport'
    
    @staticmethod
    def check(value):
        '''
        Check if the value is a valid port
        We just check if the value a single port or a range
        Values must be between 0 and 65535
        '''
        if isinstance(value, tuple):
            if len(value) == 2 and value[0] < value[1] and 0 < value[0] <= 65535 and 0 < value[1] <= 65535:
                return True;
        else:
            if 0 < value <= 65535:
                return True
            
        return False

DURATION_RE = re.compile('^(\d+)([hms]?)$')
DURATION_INFINITE = -1
# Read: (one or more digits)(optionally followed by a h, m or s)
class Duration(BaseType):
    '''
    Duration type

    Can be assigned a string or a number. Will always be read as a number.
    '''
    NAME = 'duration'

    @staticmethod
    def check(value):
        if isinstance(value, (int, long)):
            if value == DURATION_INFINITE:
                return True
            elif value >= 0:
                return True
        elif isinstance(value, basestring):
            if DURATION_RE.match(value):
                return True
        return False

    def __set__(self, obj, value):
        value = self._convertValueToSeconds(value)
        BaseType.__set__(self, obj, value)

    def _convertValueToSeconds(self, value):
        """Translate a string representation of a duration to an int
        representing the amount of seconds.

        Understood formats:
        - #h hours
        - #m minutes
        - #s seconds

        @param value: number or string representation of a duration in the above format
        @type value: string or int
        @return: amount of seconds
        @rtype: int
        """
        if not isinstance(value, basestring):
            return value
        m = DURATION_RE.match(value)
        if m:
            # Ok, valid format
            amount, granularity = m.groups()
            amount = int(amount)
            if granularity == 'h':
                multiplier = 60*60
            elif granularity == 'm':
                multiplier = 60
            elif granularity == 's':
                multiplier = 1
            else:
                # Default to seconds
                multiplier = 1
            return amount * multiplier
        return value