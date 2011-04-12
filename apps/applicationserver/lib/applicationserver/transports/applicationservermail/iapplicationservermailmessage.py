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
 
import re
import sys
import email
import email.message
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase

import json
import xmlrpclib

from twisted.python import components, log

from zope.interface import Interface, Attribute, implements

from applicationserver.iapplicationserverrequest import \
        IApplicationserverRequest
from task import Task

SPLITCHAR= '*'
KEY_VAL_SEPARATOR = '='
COMMENTCHAR = '#'

class InvalidSectionException(Exception):
    pass

class ResultParseException(Exception):
    pass

class IApplicationserverMailMessage(Interface):
    def getTasks():
        '''Parse tasks from a mail message

        @returns: List of tasks defined in the message
        @rtype: iterable
        '''

    def reply():
        '''Return an IApplicationserverMailMessage a reply'''

    subject = Attribute('Message subject')
    sender = Attribute('Message sender address')
    to = Attribute('Message reply-to address')
    reply_to = Attribute('Message reply-to address')
    delivered_to = Attribute('Message delivered-to address')
    body = Attribute('Message raw body')
    _attachments = Attribute('Message attachments, if any')

    original_message = Attribute('Original message string')

class ApplicationserverMailMessageBase(object):
    def getTasks(self):
        tasks = list()
        for section in self._genSections():
            tasks.append(self._getTask(section))
        return tasks

    def reply(self):
        sender = self.delivered_to
        if sender is None:
            if not len(self.to.split(',')) > 1:
                sender = self.to
            else:
                log.msg("Could not guess own address")
                sender = None
        m = ApplicationserverMailMessage(
            sender=sender,
            to=self.reply_to,
            subject="Re: %s" % self.subject
        )
        m.attach(self)
        return m

    def _genSections(self):
        for lines in self._genSectionLines():
            yield Section(lines)

    def _genSectionLines(self):
        current = list()
        for line in self.body.splitlines():
            if line.startswith(SPLITCHAR):
                if current:
                    yield current
                current = list()
            else:
                current.append(line)
        if current:
            yield current

    def _getTask(self, section):
        return Task(
            section.head[Section.SERVICE_KEY],
            section.head[Section.METHOD_KEY],
            section.head.get(Section.LOGIN_KEY),
            section.head.get(Section.PASSWORD_KEY),
            section.args,
            returnformat=section.head.get('returnformat', None)
        )

    def attach(self, attachment):
        self._attachments.append(attachment)

class ApplicationserverMailMessageFromEmailMessageAdapter( \
        ApplicationserverMailMessageBase):

    implements(IApplicationserverMailMessage)

    def __init__(self, message):
        self.original_message = message
        self.subject = message['Subject'] or ""
        self.sender = message['From'] or ""
        self.to = message['To']
        self.reply_to = message['Reply-To'] or self.sender
        self.delivered_to = message['Delivered-To']
        self._attachments = list()
        if message.is_multipart():
            body = message.get_payload()[0]
            if body.is_multipart():
                raise ValueError("Multipart-in-multipart is not supported")
            self.body = body.get_payload()
        else:
            self.body = message.get_payload()

components.registerAdapter(ApplicationserverMailMessageFromEmailMessageAdapter,
        email.message.Message, IApplicationserverMailMessage)

class ApplicationserverMailMessage(ApplicationserverMailMessageBase):
    implements(IApplicationserverMailMessage)

    def __init__(self, sender, to, subject):
        self.sender = sender
        self.to = to
        self.reply_to = self.sender
        self.subject = subject
        self.body = ''
        self.delivered_to = None
        self._attachments = list()

    @property
    def original_message(self):
        if len(self._attachments) > 0:
            m = MIMEMultipart()
            m.attach(MIMEText(self.body))
            for attachment in self._attachments:
                if isinstance(attachment, ApplicationserverMailMessageBase):
                    mime = ("message", "rfc822")
                    # Really weird, but the payload must be in a list...
                    payload = [attachment.original_message]
                    filename = None
                elif isinstance(attachment, XmlAttachment):
                    mime = attachment.mime
                    payload = attachment.asXml()
                    filename = attachment.filename
                else:
                    # Could use some improvement
                    raise ValueError("Unknown attachment type")
                part = MIMEBase(*mime)
                part.set_payload(payload)
                if filename is not None:
                    part.add_header('Content-Disposition',
                                    'attachment; filename="%s"' % filename)
                m.attach(part)
        else:
            m = email.message.Message()
            m.set_payload(self.body)
        m['To'] = self.to
        m['From'] = self.sender
        m['Reply-To'] = self.reply_to
        m['Subject'] = self.subject
        return m

class ApplicationserverRequestFromTask:
    implements(IApplicationserverRequest)

    def __init__(self, task):
        self.user_authenticated = False
        self.client_ip = None
        self.username = task.username
        self.password = task.password

components.registerAdapter(ApplicationserverRequestFromTask, Task,
        IApplicationserverRequest)

class Section(object):
    LOGIN_KEY = 'login'
    PASSWORD_KEY = 'password'
    SERVICE_KEY = 'category'
    METHOD_KEY = 'action'
    _FORCED_HEAD_KEYS = (SERVICE_KEY, METHOD_KEY)
    _HEAD_KEYS = (SERVICE_KEY, METHOD_KEY, LOGIN_KEY, PASSWORD_KEY, 'returnformat')

    def __init__(self, lines):
        self.lines = lines
        self.head = dict()
        self.args = dict()
        HEAD, ARGS = 1, 2
        part = HEAD

        for line in lines:
            if line.lstrip().startswith(COMMENTCHAR) or not line.strip():
                continue
            elif part == HEAD:
                key, value = self._split(line)
                if key not in self._HEAD_KEYS:
                    # We started the args
                    part = ARGS
                    self.args[key] = self._convert(value)
                else:
                    self.head[key] = value
            else:
                key, value = self._split(line)
                self.args[key] = self._convert(value)

        for key in self._FORCED_HEAD_KEYS:
            if key not in self.head:
                raise InvalidSectionException("Missing parameter '%s' in section:\n%s" % (key, self.getRaw()))

        if self.LOGIN_KEY in self.head:
            if self.PASSWORD_KEY not in self.head:
                raise InvalidSectionException("Section has parameter '%s' but lacks parameter '%s':\n%s" % (self.LOGIN_KEY, self.PASSWORD_KEY, self.getRaw()))
        if self.PASSWORD_KEY in self.head:
            if self.LOGIN_KEY not in self.head:
                raise InvalidSectionException("Section has parameter '%s' but lacks parameter '%s':\n%s" % (self.PASSWORD_KEY, self.LOGIN_KEY, self.getRaw()))

    def _split(self, line):
        if KEY_VAL_SEPARATOR not in line:
            raise InvalidSectionException("Invalid line:\n%s\nin section:\n%s" % (line, self.getRaw()))
        key, value = line.split(KEY_VAL_SEPARATOR, 1)
        return key.strip(), value.strip()

    def _convert(self, value):
        try:
            converted_value = json.loads(value)
        except ValueError, ex:
            converted_value = value.strip() # Default to string
        return converted_value


    def getRaw(self):
        return "\n".join(self.lines)

class XmlAttachment(object):
    mime = ('application', 'xml')
    def __init__(self, objects, filename):
        if not isinstance(objects, list):
            raise ValueError("Expected list object for XmlAttachment but got %s" % objects)
        self.objects = objects
        self.filename = filename

        # Parse to xml now, so errors can be reported in the mail that is sent by the transport
        try:
            self._xml = xmlrpclib.dumps((self.objects,), methodresponse=True)
        except TypeError, ex:
            raise ResultParseException("Unable to marshal some results: %s" % ex)
        except AssertionError, ex:
            raise ResultParseException("Unable to convert results to XML: %s" % ex)
        except Exception, ex:
            raise ResultParseException("Unable to convert results to XML. Unknown error: %s" % ex)

    def asXml(self):
        return self._xml
