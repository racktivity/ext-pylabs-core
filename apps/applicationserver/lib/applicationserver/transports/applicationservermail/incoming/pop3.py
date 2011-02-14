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
 
from cStringIO import StringIO
import email

from twisted.plugin import IPlugin
from twisted.mail import pop3client
from twisted.internet import reactor, protocol, defer, ssl

from zope.interface import implements

from applicationserver.transports.applicationservermail.retriever import IMailRetrieverFactory, IMailRetriever

class POP3DownloadProtocol(pop3client.POP3Client):
    # permit logging without encryption
    allowInsecureLogin = True 

    def serverGreeting(self, greeting):
        pop3client.POP3Client.serverGreeting(self, greeting)
        login = self.login(self.factory.username, self.factory.password)
        login.addCallback(self._loggedIn)
        login.chainDeferred(self.factory.deferred)

    def _loggedIn(self, result):
        return self.listSize().addCallback(self._gotMessageSizes)

    def _gotMessageSizes(self, sizes):
        retreivers = []
        for i in range(len(sizes)):
            retreivers.append(self.retrieve(i).addCallback(
                self._gotMessageLines))
        return defer.DeferredList(retreivers).addCallback(
            self._finished)

    def _gotMessageLines(self, messageLines):
        self.factory.handleMessage("\r\n".join(messageLines))

    def _finished(self, downloadResults):
        return self.quit()

class POP3DownloadFactory(protocol.ClientFactory):
    protocol = POP3DownloadProtocol
        
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.parsedMessages = list()
        self.deferred = defer.Deferred()
        self.deferred.addCallback(self._returnMessages)

    def _returnMessages(self, _tmp):
        return self.parsedMessages

    def handleMessage(self, messageData):
        parsedMessage = email.message_from_string(messageData)
        self.parsedMessages.append(parsedMessage)

    def clientConnectionFailed(self, connection, reason):
        self.deferred.errback(reason)

class POP3MailRetriever(object):
    implements(IMailRetriever)

    def __init__(self, server, username, password, ssl):
        self.server = server
        self.username = username
        self.password = password
        self.ssl = ssl

    def getMails(self):
        f = POP3DownloadFactory(self.username, self.password)

        if ssl:
            reactor.connectSSL(self.server, 995, f, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(self.server, 110, f)

        d = defer.Deferred()
        f.deferred.chainDeferred(d)
        return d

class POP3MailRetrieverFactory(object):
    implements(IPlugin, IMailRetrieverFactory)

    PROTOCOL = 'POP3'

    def getRetriever(self, account):
        return POP3MailRetriever(**account)

POP3MailRetrieverFactory_ = POP3MailRetrieverFactory()