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
from pylabs.baseclasses import BaseType

import urlparse

from Page import Page

class AttachmentProxy(BaseType):
    """A proxy representing attachment object"""

    comment = q.basetype.string(doc = "Attachment comment", allow_none = True)
    contentType = q.basetype.string(doc = "Attachment content type", allow_none = True)
    created = q.basetype.string(doc = "Attachment created at", allow_none = True)
    creator = q.basetype.string(doc = "Attachment creator", allow_none = True)
    fileName = q.basetype.string(doc = "Attachment fileName", allow_none = True)
    fileSize = q.basetype.string(doc = "Attachment fileSize", allow_none = True)
    id = q.basetype.string(doc = "Attachment Id", allow_none = True)
    pageId = q.basetype.string(doc = "Attachment pageId", allow_none = True)
    title = q.basetype.string(doc = "Attachment title", allow_none = True)
    url = q.basetype.string(doc = "Attachment url", allow_none = True)
    version = q.basetype.string(doc = "Attachment version", allow_none = True) #only specified as a parameter in url

    def __init__(self, attachmentDict):
        BaseType.__init__(self)
        self.version = None
        for key, value in attachmentDict.iteritems():
            setattr(self, key, str(value))
        self.version = urlparse.parse_qs(urlparse.urlparse(self.url).query)['version'][0]
        #self.version = self.url.rsplit('=',1)[1] #version is only specified as a parameter in the url


    def toDict(self):
        """Construct a dictionary representing attachment object values

        @rtype: dictionary"""
        variables = ('comment', 'contentType', 'created', 'creator', 'fileName', 'fileSize', 'id', 'pageId', 'title', 'url', 'version')
        return dict((key, getattr(self, key)) for key in variables if getattr(self, key) is not None)

    def __repr__(self):
        return str(self.toDict())
