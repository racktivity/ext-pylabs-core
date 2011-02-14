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
import email
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from twisted.internet import reactor, defer
from twisted.mail.smtp import ESMTPSenderFactory
from twisted.python import log
from twisted.internet.ssl import ClientContextFactory

from OpenSSL.SSL import TLSv1_METHOD

class ApplicationserverSMTPSender(object):
    def __init__(self, server, username, password, ssl, address, port=None):
        self.server = server
        self.username = username
        self.password = password
        self.ssl = ssl
        self.address = self._getRawAddress(address)
        self.port = port

    def _getRawAddress(self, fancyAddress):
        raw_addresses = list()
        for fullAddr in fancyAddress.split(","):
            name, raw = email.Utils.parseaddr(fullAddr)
            raw_addresses.append(raw)
        if len(raw_addresses) == 1:
            return raw_addresses[0]
        return raw_addresses

    def send(self, mail):
        # mail is of email module
        d = defer.Deferred()
        senderArgs = {
            'username': self.username,
            'password': self.password,
            'fromEmail': self.address,
            'toEmail': self._getRawAddress(mail['To']),
            'file': StringIO(str(mail)),
            'deferred': d,
            'retries': 5,
        }
        if self.ssl:
            senderArgs['contextFactory'] = ClientContextFactory()

        sender = ESMTPSenderFactory(**senderArgs)

        if self.ssl:
            port = self.port or 465
            reactor.connectSSL(self.server, port, sender, ClientContextFactory())
        else:
            port = self.port or 25
            reactor.connectTCP(self.server, port, sender)

        d.addCallback(self.sent)
        d.addErrback(self.fail)

    def sent(self, result):
        log.msg('Mail sent: %s' % str(result))

    def fail(self, reason):
        log.err('Failed to send mail: %s' % reason)

if __name__ == '__main__':
    import email.message

    m = email.message.Message()
    m['To'] = 'alice@server.com'
    m['From'] = 'bob@otherserver.com'
    m.set_payload("This is the mail body.")
    m['Subject'] = 'This is the mail subject'

    s = ApplicationserverSMTPSender('smtp.otherserver.com', 'bob', 'secret', False)
    s.send(m)
    reactor.run()