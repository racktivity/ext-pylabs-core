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
 
"""
This module is the heart of the mail transport. It contains the MailTransport
object. This object in its turn creates the incoming and outgoing mail
'transports'. The incoming mail transports are in the 'incoming' subfolder.
The outgoing mail transports are in the 'outgoing' subfolder.

This module works with 'Mails' and 'Tasks'. Mails are handled concurrently
by the MailProcessor. One Mail contains at least one Task. Tasks from the
same Mail are executed one after the other. If one Task of a Mail fails,
the Tasks following that failing Task are _not_ executed.

The whole system starts with the fill method of the MailTransport. This method
fills a DeferredQueue with Mail objects it retrieves from the incoming
transport.

These Mails are handled by the MailProcessor. The MailProcessor fetches Mails
from the DeferredQueue, extracts the tasks from them and hands over the work
to the TaskProcessor. It then immediately tries to fetch the next mail from
the DeferredQueue. This enables multiple Mails to be executed concurrently.

The TaskProcessor then executes the Tasks one after the other and calls back
the MailProcessor when an error occurs or all Tasks were executed.

Notes:
    - The taskMethod is handed from MailTransport to MailProcessor to 
      TaskProcessor. This isn't very clean.
    - The deferred-related code in MailProcessor and TaskProcessor should
      be improved. TaskProcessor shouldn't inherit from Deferred, it should
      use a Deferred attribute instead.
    - A lot of info is now passed to the TaskProcessor from the MailProcessor
      because the MailProcessor needs it when the control flow is handed back
      to it. This should change. Maybe use inner functions in the MailProcessor
      to connect to the Deferred of the TaskProcessor?
    - There is some code duplication in the MailProcessor related to return
      formats.
    - A send method is passed to the MailProcessor. It might be better to solve
      this in an other way.
"""

import sys
import traceback
import operator

from twisted.plugin import IPlugin, getPlugins
from twisted.internet import threads, defer, reactor
from twisted.python import components, failure, log

from zope.interface import implements

from applicationserver.itransport import ITransport
from applicationserver.iapplicationserverrequest import IApplicationserverRequest
from applicationserver import cronjob, CRON_JOB_STOP, crond

from applicationserver.dispatcher import NoSuchService, AuthenticationError, NoSuchMethod
from applicationserver.transports.applicationservermail.retriever import IMailRetrieverFactory
from applicationserver.transports.applicationservermail import \
    iapplicationservermailmessage
from applicationserver.humanreadable import HumanReadable
from applicationserver import iapplicationserverrequest
from applicationserver.itransport import TransportInfo

from task import Task
from mailtemplates import generate_json_body, generate_hr_body, generate_process_error, generate_error, generate_json_error, generate_timeout, generate_unknown_parse_error
import incoming
from outgoing.smtp import ApplicationserverSMTPSender

RESULT_ATTACHMENT_FILENAME = 'response.xml'
HR_FORMAT = 'HR'
XML_FORMAT = 'XML'
JSON_FORMAT = 'JSON'
MAIL_TIMEOUT_WARNING = 30*60 # 30 minutes

class TaskFailure(failure.Failure):
    """
    Custom Failure used to pass information about failed Tasks from the
    TaskProcessor to the MailProcessor
    """
    def __init__(self, reason, mail, task, tasks, results, format):
        failure.Failure.__init__(self, exc_value=reason)
        self.mail = mail
        self.task = task
        self.tasks = tasks
        self.results = results
        self.format = format

class TaskProcessor(defer.Deferred):
    """
    Processes tasks from a task list, stops processing if one task fails or
    if all tasks finished correctly.
    """
    def __init__(self, mail, tasks, taskMethod):
        """
        @param mail: mail to be passed when returning
        @type mail: applicationserver.transports.applicationservermail.iapplicationservermailmessage.ApplicationserverMailMessageBase
        @param tasks: a list of tasks
        @type tasks: list of L{applicationserver.transports.applicationservermail.task.Task}
        @param taskMethod: method to execute tasks with (dispatcher.callServiceMethod)
        @type taskMethod: callable
        """
        defer.Deferred.__init__(self)
        self.mail = mail
        # Save the original task list to be able to return it later
        self.tasks = tasks
        # Enable iterating the task list in this processor
        self.task_iter = iter(tasks)
        self.taskMethod = taskMethod
        self.results = list()
        # Default to human readable format
        self.format = self.tasks[0].returnformat or HR_FORMAT
        self.human_readable = bool(self.format == HR_FORMAT)

    def run(self):
        self.next(None, self.task_iter.next())

    def next(self, _tmp, task):
        self.current_task = task

        kwargs = task.kwargs
        request = iapplicationserverrequest.IApplicationserverRequest(task)

        try:
            d = self.taskMethod(request, task.service, task.method,
                                __applicationserver_human_readable=self.human_readable, **kwargs)
            d.addCallback(self.addResult)
            try:
                nextTask = self.task_iter.next()
            except StopIteration:
                # current_task is the last task; When the last task is finished
                # we need to start our callback chain
                d.addCallback(self.callback)
            else:
                # current_task is not the lat task; start the next task when
                # current_task is finished
                d.addCallback(self.next, nextTask)
            d.addErrback(self.errback)
            # TODO: return nextTask, remove the _tmp arg from next()
        except NoSuchService, ex:
            msg = "No category '%s' registered on this server" % task.service
            self.errback(msg)
        except NoSuchMethod, ex:
            msg = "No action '%s' was found in category '%s'" % (task.method, task.service)
            self.errback(msg)
        except AuthenticationError, ex:
            log.msg("Authentication error: %s" % ex)
            msg = "An authentication error occurred"
            self.errback(msg)
        except Exception, ex:
            log.msg("Unknown exception before executing '%s': %s" % (task, ex))
            self.errback(ex)

    def callback(self, _tmp=None):
        # Inject the original mail and tasks with the results and the format
        # in the callback chain
        return defer.Deferred.callback(self, (self.mail, self.tasks, self.results, self.format))

    def addResult(self, result):
        """Log the result and append it to the results list"""
        # Weird construct to catch exceptions thrown in the __str__ method of
        # the result.
        try:
            log.msg("%s returned result %s" % (self.current_task, result))
        except Exception, ex:
            log.err("Could not log result: %s" % ex)

        self.results.append(result)

    def errback(self, reason):
        # Inject a custom failure into the errback chain
        f = TaskFailure(reason, self.mail, self.current_task, self.tasks, self.results, self.format)
        return defer.Deferred.errback(self, f)

class MailProcessor(object):
    """
    Fetches Mails from a DeferredQueue, extracts the Tasks from those Mails and
    passes them to the TaskProcessor. The MailProcessor also handles sending
    the result of executing the tasks back to the user.
    """
    def __init__(self, mailQueue, taskMethod, send):
        """
        @param mailQueue: Queue containing Mails that need processing
        @type mailQueue: twisted.internet.defer.DeferredQueue
        @param taskMethod: method to execute the Tasks with, will be passed to each TaskProcessor
        @type taskMethod: callable
        @param send: 
        @type send: callable
        """
        self.mailQueue = mailQueue
        self.taskMethod = taskMethod
        self.send = send
        self.next()

    def next(self, tmp=None):
        d = self.mailQueue.get()
        d.addCallback(
            self.process
        )
        # Note: process expects reply as its callback so it can return None when an error was handled
        d.addCallback(self.next)

    def reply(self, result, timeoutCall):
        if timeoutCall.active():
            timeoutCall.cancel()

        if result is None:
            return
        mail, tasks, results, format = result
        reply = mail.reply()
        body = ""

        xml_attachment = None
        msg = None
        try:
            if results and isinstance(results[0], HumanReadable):
                origResults = [result.original for result in results]
            else:
                origResults = results
            xml_attachment = iapplicationservermailmessage.XmlAttachment(origResults, RESULT_ATTACHMENT_FILENAME)
        except ValueError, ex:
            msg = "Could not attach results to reply mail: %s\n\n" % ex
        except iapplicationservermailmessage.ResultParseException, ex:
            msg = "Could not attach results to reply mail because the results could not be parsed: %s\n\n" % ex
        except:
            msg = "Could not attach results to reply mail because of an unknown error\n\n"
        finally:
            if msg:
                log.err(msg)
                body += "\n%s" % msg
        
        if format == XML_FORMAT:
            # Body will be empty when no error occurred, so body will be valid xml after next line
            # Body will contain an error message when xml transformation failed
            body += xml_attachment.asXml() or ""
        elif format == JSON_FORMAT:
            # Overwrite possible xml error messages because these would invalidate the JSON
            body = generate_json_body(results)
        else:
            if format != HR_FORMAT:
                self.unknownFormat(format, HR_FORMAT)
            body += generate_hr_body(tasks, results)

        reply.body = body
        if xml_attachment:
            reply.attach(xml_attachment)

        self.send(reply)

    def process(self, mail):
        try:
            tasks = mail.getTasks()
        except iapplicationservermailmessage.InvalidSectionException, ex:
            self.handleProcessError(mail, ex)
            return
        except Exception, ex:
            log.msg("An unknown parse error occurred. Notifying user...: %s" % ex)
            self.handleUnknownParseError(mail)
            log.msg("User was notified")
            return

        tp = TaskProcessor(mail, tasks, self.taskMethod)
        tp.run()
        tp.addErrback(self.taskFailed)
        timeoutCall = reactor.callLater(MAIL_TIMEOUT_WARNING, self.mailTimeout, mail)
        tp.addCallback(self.reply, timeoutCall)

    def handleProcessError(self, mail, ex):
        reply = mail.reply()
        reply.body = generate_process_error(ex)
        self.send(reply)

    def handleUnknownParseError(self, mail):
        reply = mail.reply()
        reply.body = generate_unknown_parse_error()
        self.send(reply)

    def mailTimeout(self, mail):
        reply = mail.reply()
        reply.body = generate_timeout(MAIL_TIMEOUT_WARNING)
        self.send(reply)

    def unknownFormat(format, default):
        log.err("Unknown return format '%s', defaulting to '%s'" % (format, default))
    
    def taskFailed(self, reason):
        # reason = TaskFailure
        errorMail = reason.mail.reply()
        errorTask = reason.task
        allTasks = reason.tasks
        results = reason.results
        format = reason.format
        errorIndex = allTasks.index(errorTask)
        error_nr = getattr(reason.value, 'ERRNO', 8002)

        # Create a Fault struct
        fault = {
            'faultCode': error_nr,
            'faultString': reason.getErrorMessage(),
        }
        all_results = list(results)
        all_results.append(fault)

        xml_attachment = None
        body = ""
        try:
            xml_attachment = iapplicationservermailmessage.XmlAttachment(all_results, RESULT_ATTACHMENT_FILENAME)
        except ValueError, ex:
            msg = "Could not attach results to reply mail."
            log.err(msg)
            log.err(ex)
            body += msg
        except iapplicationservermailmessage.ResultParseException, ex:
            msg = "Could not attach results to reply mail."
            log.err(msg)
            log.err(ex)
            body += msg

        if format == XML_FORMAT:
            # Body will be empty when no error occurred, so body will be valid xml after next line
            # Body will contain an error message when xml transformation failed
            if xml_attachment:
                body += xml_attachment.asXml()
        elif format == JSON_FORMAT:
            body = generate_json_error(results, error_nr, reason.getErrorMessage())
        else:
            if format != HR_FORMAT:
                self.unknownFormat(format, HR_FORMAT)
            context = {
                'task_nr': errorIndex + 1,
                'results': results,
                'tasks': allTasks,
                'errortask': errorTask,
                'error_nr': error_nr,
                'error_msg': reason.getErrorMessage(),
            }
            body += generate_error(**context)

        errorMail.body = body
        if xml_attachment:
            errorMail.attach(xml_attachment)
        self.send(errorMail)
        # Log that we handled this exception. The exception output (traceback) was printed to console when it happened.
        log.err("Exception in task %s was handled" % errorTask)

class MailTransport:
    implements(ITransport)

    def __init__(self, dispatcher, interval, protocol, address, incoming_account, outgoing_account):
        self.dispatcher = dispatcher
        self.interval = interval
        self.address = address
        self.incoming = self.getIncoming(protocol, incoming_account)
        self.outgoing = ApplicationserverSMTPSender(address=self.address, **outgoing_account)
        self.mailQueue = defer.DeferredQueue(size=100)
        self.mailProcessor = MailProcessor(self.mailQueue, taskMethod=self.dispatcher.callServiceMethod, send=self.sendMail)
        self.mailCache = list()
        self.run()

    def run(self):
        """Start the cron cycle"""
        self.fill = cronjob(self.interval)(self.fill)
        crond.addService('__applicationserver_mail', self)
        
    def fill(self, o):
        d= self.incoming.getMails()
        d.addCallback(self._queueMails)
        d.addErrback(self._handleError)

    def _queueMails(self, mails):
        if mails is None:
            # Got here through the errback
            return
        self.mailCache.extend(mails)
        try:
            for x in xrange(len(self.mailCache)):
                email = self.mailCache[0]
                mail = iapplicationservermailmessage.IApplicationserverMailMessage(email)
                self.mailQueue.put(mail)
                self.mailCache.pop(0)
        except defer.QueueOverFlow:
            # The mail is still in the mailCache, nothing to do
            pass

    def _handleError(self, reason):
        log.err("Failed to fetch mail(s)")
        log.err("Traceback:\n%s" % reason.getTraceback())

    def _tickFailure(self, reason):
        raise reason

    def getIncoming(self, protocol, account):
        known_retriever_factories = getPlugins(IMailRetrieverFactory, incoming)
        for factory in known_retriever_factories:
            if factory.PROTOCOL == str(protocol):
                return factory.getRetriever(account)
        raise Exception("No matching incoming mail protocol found for protocol name '%s'" % protocol)

    def sendMail(self, mail):
        # mail is of class Mail, translate to email
        self.outgoing.send(mail.original_message)

    def getTransportInfo(self, name):
        return MailTransportInfo(name, self.address)


from ..mail import MailTransportFactory
class MailTransportInfo(TransportInfo):
    PROTOCOL = MailTransportFactory.PROTOCOL

    def __init__(self, name, address):
        super(MailTransportInfo, self).__init__(name)
        self._address = address

    address = property(operator.attrgetter('_address'),
        doc='Configured e-mail address')