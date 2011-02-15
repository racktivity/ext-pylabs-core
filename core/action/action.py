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
import inspect
import textwrap
import operator

import pylabs
from pylabs.decorators import deprecated

class StartStopOutputCountException(Exception):
    '''Exception raised when an action.startOutput/action.stopOutput count
    mismatch occurs'''
    def __init__(self):
        super(StartStopOutputCountException, self).__init__(
                'Output start/stop count mismatch')


def _deprecated_attrgetter(public_name, name):
    def _getter(self):
        '''Return attribute %(name)s'''
        pylabs.q.logger.log('[DEPRECATION] Accessing deprecated '
                              'attribute %s' % (public_name), 6)
        return getattr(self, name)

    _getter.__doc__ = _getter.__doc__ % {
        'name': name,
    }

    return _getter

class _DeprecatedArgument(object):
    '''Dummy class of which an instance is used as default argument for
    deprecated function arguments'''
    def __str__(self):
        return 'DEPRECATED'

    def __repr__(self):
        return 'DEPRECATED'

_DEPRECATED = _DeprecatedArgument()


class _ActionStatus(object):
    '''Enumeration of all known action statuses'''
    DONE = 'DONE'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'

_MAX_STATUS_LENGTH = 0
def calculateLongestStatusLength():
    '''Calculate the length of the longest action status name

    @returns: Length of longest action status name
    @rtype: number
    '''
    def actionLengths():
        for name, value in inspect.getmembers(_ActionStatus):
            if name.startswith('_'):
                continue
            yield len(value)

    global _MAX_STATUS_LENGTH
    if _MAX_STATUS_LENGTH:
        return _MAX_STATUS_LENGTH

    _MAX_STATUS_LENGTH = max(actionLengths())
    return _MAX_STATUS_LENGTH


class _Action(object):
    '''Representation of an action'''
    def __init__(self, description, errormessage, resolutionmessage, indent):
        '''Initialize a new action

        @param description: Description message displayed to the user
        @type description: string
        @param errormessage: Error message displayed when the action fails
        @type errormessage: string
        @param resolutionmessage: Resolution message displayed when the action
                                  fails
        @type resolutionmessage: string
        @param indent: Indention level of this action
        @type indent: number
        '''
        self.description = description or ''
        self.errormessage = errormessage or ''
        self.resolutionmessage = resolutionmessage or ''

        self.indent = indent
        self.interrupted = False

        self._output = ''
        self._output_start_count = 0

    def calculateMessage(self, width):
        '''Calculate the message to display to the user

        Since this can be a multiline message the length of the last line is
        returned as well.

        @param width: Maximum line width
        @type width: number

        @returns: Length of last line and message to display
        @rtype: tuple<number, string>
        '''
        maxResultLength = calculateLongestStatusLength()
        prefix = ' * %s' % (' ' * self.indent)
        maxMessageLength = width - maxResultLength - 1 - self.indent

        parts = textwrap.wrap(self.description, maxMessageLength,
                              initial_indent=prefix,
                              subsequent_indent='%s ' % prefix)
        return len(parts[-1]), '\n'.join(parts)

    def write(self, output, width):
        '''Write the description message to output

        @param output: File-like object to write to
        @type output: object
        @param width: Maximum line width
        @type width: number
        '''
        _, msg = self.calculateMessage(width)
        output.write(msg)
        output.flush()

    def writeResult(self, output, result, width):
        '''Write the result of the current action

        The action description will be printed again if the action was
        interrupted as well.

        @param output: File-like object to write to
        @type output: object
        @param result: Action result
        @type result: string
        @param width: Maximum line width
        @type width: number
        '''
        if self.interrupted:
            self.write(output, width)

        longestResultLength = calculateLongestStatusLength()

        len_, _ = self.calculateMessage(width)
        spacing = width - len_ - longestResultLength - 1
        spacing = max(spacing, 1)
        output.write('%s%s\n' % (' ' * spacing, result))
        output.flush()

    def _setOutput(self, value):
        #TODO We might want to deprecate this one day
        self._output = value

    output = property(fget=operator.attrgetter('_output'), fset=_setOutput)

    # We need these aliases until the event subsystem no longer uses these
    # attributes (or accesses the protected list of running actions at all)
    errorMessage = property(fget=_deprecated_attrgetter(
                                    '_Action.errorMessage', 'errormessage'))
    resolutionMessage = property(
        fget=_deprecated_attrgetter(
                                    '_Action.resolutionMessage',
                                    'resolutionmessage'))

    def increaseOutputCount(self):
        '''Increase the counter counting the number of calls to
        action.startOutput during this action'''
        self._output_start_count += 1

    def decreaseOutputCount(self):
        '''Decrease the counter counting the number of calls to
        action.startOutput during this action, i.e. on every call to
        action.stopOutput

        @raise StartStopOutputCountException: Count became negative
        '''
        self._output_start_count -= 1
        if self._output_start_count < 0:
            raise StartStopOutputCountException

    def checkOutputCountIsZero(self):
        '''Check whether the counter counting the number of calls to
        action.startOutput minus the number of calls to action.stopOutput during
        this action is zero, i.e. the number of calls to action.startOutput
        matches the number of calles to action.stopOutput, as it should

        @raise StartStopOutputCountException: Count is not equal to 0
        '''
        if self._output_start_count != 0:
            raise StartStopOutputCountException


class ActionController(object):
    '''Manager controlling actions'''
    def __init__(self, _output=None, _width=70):
        '''Initialize a new action controller

        @param _output: File-like object to write output to. Defaults to
                        sys.stdout.
                        This should not be used by anyone except testcases
        @type _output: object
        @param _width: Maximum width of output
                       This should not be used by anyone except testcases
        @type _width: number
        '''
        self._actions = list()
        self._output = _output or sys.stdout
        self._width = _width

        self._output_start_count = 0

    def start(self, description, errormessage=None, resolutionmessage=None,
              show=_DEPRECATED, messageLevel=_DEPRECATED):
        '''Start a new action

        @param description: Description of the action
        @type description: string
        @param errormessage: Error message displayed to the user when the action
                             fails
        @type errormessage: string
        @param resolutionmessage: Resolution message displayed to the user when
                                  the action fails
        @type resolutionmessage: string
        '''
        #TODO Be more verbose / raise in time
        if show is not _DEPRECATED:
            pylabs.q.logger.log('[ACTIONS] Using deprecated/unused argument '
                                  '\'show\'', 4)
        if messageLevel is not _DEPRECATED:
            pylabs.q.logger.log('[ACTIONS] Using deprecated/unused argument '
                                  '\'messageLevel\'', 4)

        if self._actions and not self._actions[-1].interrupted:
            self._actions[-1].writeResult(self._output, _ActionStatus.RUNNING,
                                           self._width)
            self._actions[-1].interrupted = True

        pylabs.q.logger.log('[ACTIONS] Starting action: %s' % description,
                              5)
        action = _Action(description, errormessage, resolutionmessage,
                        indent=len(self._actions))
        self._actions.append(action)

        action.write(self._output, self._width)

        #TODO Get rid of this when reworking console handling properly
        pylabs.q.console.hideOutput()

    def stop(self, failed=False):
        '''Stop the currently running action

        This will get the latest started action from the action stack and
        display a result message.

        @param failed: Whether the action failed
        @type failed: bool
        '''
        if not self._actions:
            #TODO Raise some exception?
            pylabs.q.logger.log('[ACTIONS] Stop called while no actions are '
                                  'running at all', 3)
            return

        action = self._actions.pop()

        # If this is the last action, _output_start_count should be 0
        if not self._actions:
            if not self._output_start_count == 0:
                self._output_start_count = 0
                #raise StartStopOutputCountException
                self._handleStartStopOutputCountMismatch()

        try:
            action.checkOutputCountIsZero()
        except StartStopOutputCountException:
            self._handleStartStopOutputCountMismatch()

        status = _ActionStatus.DONE if not failed else _ActionStatus.FAILED
        if not failed and not self._actions and action.interrupted:
            status = _ActionStatus.FINISHED
        pylabs.q.logger.log('[ACTIONS] Stopping action \'%s\', result '
                              'is %s' % (action.description, status), 5)
        action.writeResult(self._output, status, self._width)

        if not self._actions:
            #TODO Get rid of this when reworking console handling properly
            pylabs.q.console.showOutput()

    def clean(self):
        '''Clean the list of running actions'''
        pylabs.q.logger.log('[ACTIONS] Clearing all actions', 5)
        self._actions = list()
        #TODO Get rid of this when reworking console handling properly
        pylabs.q.console.showOutput()

    def hasRunningActions(self):
        '''Check whether actions are currently running

        @returns: Whether actions are runnin
        @rtype: bool
        '''
        return bool(self._actions)


    @deprecated('q.action.printOutput', version='3.2')
    def printOutput(self):
        for qa in self._runningActions:
            self._output.write('%s\n' % qa.output)


    @deprecated('q.actions._runningActions', version='3.2')
    def _setActions(self, value):
        self._actions = value

    _runningActions = property(fget=operator.attrgetter('_actions'),
                               fset=_setActions)


    def startOutput(self):
        """
        Enable q.console output. Format such that it is nicely shown between action start/stop.
        """
        pylabs.q.console.showOutput()

        self._output_start_count += 1
        if self.hasRunningActions():
            self._actions[-1].increaseOutputCount()

        if self.hasRunningActions() and not self._actions[-1].interrupted:
            # After a START, must make sure to put the last action on "RUNNING"
            self._actions[-1].writeResult(self._output, _ActionStatus.RUNNING,
                                           self._width)
            self._actions[-1].interrupted = True

    def stopOutput(self):
        """
        Disable q.console output. Format such that it is nicely shown between action start/stop.
        """
        if self.hasRunningActions():
            try:
                self._actions[-1].decreaseOutputCount()
            except StartStopOutputCountException:
                self._handleStartStopOutputCountMismatch()
                return

        self._output_start_count -= 1
        if self._output_start_count < 0:
            self._output_start_count = 0
            #raise StartStopOutputCountException
            self._handleStartStopOutputCountMismatch()

        if self.hasRunningActions() and (self._output_start_count == 0):
            pylabs.q.console.hideOutput()


    def _handleStartStopOutputCountMismatch(self):
        '''Handle a start/stop output count mismatch exception

        Reset running action list and output start count.

        This will break running actions or might break future actions.
        '''
        pylabs.q.logger.log(
            '[ACTIONS] Warning: start/stop output count mismatch', 4)
        self._actions = list()
        self._output_start_count = 0