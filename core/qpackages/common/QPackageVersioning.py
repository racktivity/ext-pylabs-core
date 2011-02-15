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

class QPackageVersioning(object):
    @staticmethod
    def versionCompare(version1, version2):
        """
        Compare two QPackage versions e.g. 1.2.4, 1.4.1
        Only dot separated numeric values are allowed.
        First split both lists, then compares each value starting from the most significant value
        @param version1: dot seperated numeric string
        @param version2: dot seperated numeric string
        """
        splitVersion1 = version1.split('.')
        splitVersion2 = version2.split('.')
        q.logger.log('Checking if both list have the same length. Padding the smaller list..', 7)
        if len(splitVersion1) > len(splitVersion2):
            splitVersion2.extend(['0' for i in xrange(len(splitVersion1)-len(splitVersion2))])
        elif len(splitVersion2) > len(splitVersion1):
            splitVersion1.extend(['0' for i in xrange(len(splitVersion2)-len(splitVersion1))])

        q.logger.log('Comparing each value in the both lists', 7)
        for i in xrange(len(splitVersion1)):
            if splitVersion1[i] != splitVersion2[i]:
                return int(splitVersion1[i]) - int(splitVersion2[i])
        return 0