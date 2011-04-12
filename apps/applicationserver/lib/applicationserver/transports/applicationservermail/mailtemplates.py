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
 
import json

from twisted.python import log

from applicationserver.humanreadable import HumanReadable

def verbosetask(t):
    return "%s:%s(%s)" % (t.service, t.method, ", ".join("%s=%s" % (k, v) for k, v in t.kwargs.iteritems()))

# Idea from http://jtauber.com/2006/05/templates.html
class Template(object):
    text = ""
    def __init__(self, **variables):
        self.variables = variables

    def __str__(self):
        try:
            return self.text % self
        except KeyError, ex:
            log.err("KeyError: %s" % ex)
            return "*VARIABLE NOT FOUND*"
        except Exception, ex:
            log.err("Failed to parse object to string: %s" % ex)
            return generate_template_error()

    def __getitem__(self, key):
        parts = key.split('|')
        variable = parts[0]
        filters = parts[1:]
        value = self.variables[variable]
        for filter in filters:
            value = self._filter(filter, value)
        return value

    def _filter(self, filtername, value):
        f = getattr(self, filtername)
        return f(value)

    def li(self, l):
        return str(ListTemplate(li=l))

    def count(self, l):
        return len(l)

class IndentTemplate(Template):
    INDENTATION = "  "
    def __init__(self, indentlevel=0, **kwargs):
        Template.__init__(self, **kwargs)
        self.indentlevel = indentlevel
        self.variables["_indent"] = self.INDENTATION * self.indentlevel

    def listitems(self, l):
        items = [str(ListItemTemplate(indentlevel=(self.indentlevel), listitem=item)) for item in l]
        return "\n".join(items)

    def dictitems(self, d):
        items = [str(DictItemTemplate(indentlevel=(self.indentlevel), key=key, value=value)) for key, value in d.iteritems()]
        return "\n".join(items)

    def smartlist(self, x):
        if isinstance(x, (list, tuple)):
            return str(ListTemplate(indentlevel=(self.indentlevel + 1), li=x))
        return x

    def smartdict(self, x):
        if isinstance(x, dict):
            return str(DictTemplate(indentlevel=(self.indentlevel + 1), di=x))
        return x

    def smart(self, x):
        return self.smartdict(self.smartlist(x))

class DictTemplate(IndentTemplate):
    text = "A structured object containing %(di|count)d items:\n%(di|dictitems)s"

class DictItemTemplate(IndentTemplate):
    text = "%(_indent)s - %(key)s: %(value|smart)s"

class ListTemplate(IndentTemplate):
    text = "A list containing %(li|count)d elements:\n%(li|listitems)s"

class ListItemTemplate(IndentTemplate):
    text = "%(_indent)s - %(listitem|smart)s"
 
class HumanReadableListItemTemplate(ListItemTemplate):
    text = "Your call %(task|verbosetask)s completed successfully and returned:\n%(result|smart)s"

    def verbosetask(self, t):
        return verbosetask(t)

class HumanReadableListItemNoneTemplate(HumanReadableListItemTemplate):
    text = "Your %(task)s completed successfully"

class HumanReadableResponseTemplate(Template):
    text = """%(tasks_results|human_readable_list)s"""

    def human_readable_list(self, l):
        lines = list()
        for task, result in l:
            if result is None:
                lines.append(HumanReadableListItemNoneTemplate(task=task, result=result))
            elif isinstance(result, HumanReadable):
                lines.append(HumanReadableListItemTemplate(task=task, result=result.human_readable))
            else:
                lines.append(HumanReadableListItemTemplate(task=task, result=result))
        return "\n\n".join(str(x) for x in lines)

    def verbosetask(self, t):
        return verbosetask(t)

class ProcessErrorTemplate(Template):
    text = """Error #8004: The request could not be understood due to malformed syntax.

Every line in the request email should be a name=value pair. At least a "service" and "action" entry \
should be included. A "login" and "password" and/or "returnformat" entry can be added optionally. The \
value of "returnformat" should be HR (Human Readable), JSON or XML. If "returnformat" is omitted, a \
human readable answer will be sent.

A second section containing parameters for the action can be added. The two sections should be \
separated by an empty line.

Example request mail
====================

category = my_service
action = example_action
login = monty
# Comment
password = python
param_a = value1
param_b = value2

Detailed info: %(exception)s
"""

class ErrorTemplate(HumanReadableResponseTemplate):
    text = """There was an error when executing task nr %(task_nr)d.

%(tasks_results|human_readable_list)s

Your call %(errortask|verbosetask)s could not be completed. Error #%(error_nr)d occurred:
%(error_msg)s
"""

# TODO: bad: magic number
ERR_NO = 8002
def generate_json_body(results):
    def stringify(x):
        return str(x)

    try:
        return json.dumps(results, default=stringify)
    except TypeError, ex:
        # Shouldn't happen because we use default=stringify
        msg = "Failed to dump one of the results to JSON format: %s" % ex
        log.err(msg)
        return "%d, %s" % (ERR_NO, msg)
    except Exception, ex:
        msg = "An unknown error occurred while parsing the results: %s" % ex
        log.err(msg)
        return "%d, %s" % (ERR_NO, msg)

def generate_json_error(results, errno, errmsg):
    local_results = list(results)
    local_results.append("Error #%d: %s" % (errno, errmsg))
    return generate_json_body(local_results)

def generate_hr_body(tasks, results):
    tasks_results = zip(tasks, results)
    return str(HumanReadableResponseTemplate(tasks_results=tasks_results))

def generate_process_error(exception):
    return str(ProcessErrorTemplate(exception=exception))

def generate_error(task_nr, tasks, results, errortask, error_nr, error_msg):
    return str(ErrorTemplate(task_nr=task_nr,
                             tasks_results=zip(tasks, results),
                             errortask=errortask,
                             error_nr=error_nr,
                             error_msg=error_msg))

def generate_timeout(duration):
    return """The task(s) in mail are taking more than %d seconds to finish. Its execution will not be interrupted. Notify an administrator if this behaviour is unexpected.""" % duration

def generate_unknown_parse_error():
    return """An unknown error occurred while parsing your email. No tasks were started. Please contact your server administrator."""

def generate_template_error():
    return """An error occurred while generating this response mail. Please contact your server administrator."""
