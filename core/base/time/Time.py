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

import pymonkey
import time


class Time:
    """
    generic provider of time functions
    lives at q.base.time
    """
    def getTimeEpoch(self):
        '''
        Get epoch timestamp (number of seconds passed since January 1, 1970)
        '''
        timestamp = int(time.time())
        return timestamp


    def getLocalTimeHR(self):
        '''Get the current local date and time in a human-readable form'''
        #timestamp = time.asctime(time.localtime(time.time()))
        timestr=self.formatTime(self.getTimeEpoch())
        return timestr

    def getLocalTimeHRForFilesystem(self):
        #@todo check if correct implementation
        return time.strftime("%d_%b_%Y_%H_%M_%S", time.gmtime())
    
    def formatTime(self,epoch,formatstr='%Y/%m/%d %H:%M:%S',local=True):
        '''
        Returns a formatted time string representing the current time

        See http://docs.python.org/lib/module-time.html#l2h-2826 for an
        overview of available formatting options.

        @param format: Format string
        @type format: string

        @returns: Formatted current time
        @rtype: string
        '''
        epoch=float(epoch)
        if local:
            timetuple=time.localtime(epoch)
        else:
            timetuple=time.gmtime(epoch)
        timestr=time.strftime(formatstr,timetuple)
        return timestr

    def epoch2HRDate(self,epoch,local=True):
        return self.formatTime(epoch,'%Y/%m/%d',local)
        
    def epoch2HRDateTime(self,epoch,local=True):
        return self.formatTime(epoch,'%Y/%m/%d %H:%M:%S',local)
        
    def epoch2HRTime(self,epoch,local=True):
        return self.formatTime(epoch,'%H:%M:%S',local)
        
        
    def HRDatetoEpoch(self,datestr,local=True):
        """
        convert string date to epoch
        Date needs to be formatted as 16/06/1988
        """
        try:
            return time.mktime(time.strptime(datestr, "%d/%m/%Y"))
        except:
            raise ValueError ("Date needs to be formatted as \"16/06/1981\"")
        
