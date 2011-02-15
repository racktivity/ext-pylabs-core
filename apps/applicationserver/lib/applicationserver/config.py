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

import os

from zope.interface import implements, Interface

class IConfigReader(Interface):
    def parseConfig():
        '''Retrieve Applicationserver configuration

        This method parses the applicationserver configuration, eg by using a
        configuration file, and returns a dictionary containing all
        configuration data to the controller.

        @return: Configuration data
        @rtype: dict

        @todo: Document dictionary format
        @todo: Consider using an object-based configuration system
        '''


class IniConfigReader:
    '''Configuration reader for INI-files'''
    implements(IConfigReader)

    def __init__(self, config_name):
        '''Initialize an INI-file configuration reader for a given file

        @param config: Configuration INI-file path
        @type config: string
        '''
        self.config_name = config_name

    def parseConfig(self):
        from pylabs_bindings import Server, SERVICE_ROOT
        from pylabs import q

        qconfig = q.config.getConfig(self.config_name)['main']

        def service_to_path(service):
            if '.' not in service:
                return service
            module, klass = service.rsplit('.', 1)
            module = "%s.py" % module.replace('.', os.sep)
            return "%s:%s" % (os.path.join(SERVICE_ROOT, module), klass)

        config = dict()
        config['name'] = 'applicationserver'

        if qconfig['xmlrpc_port']:
            config["transport_xmlrpc"] = {
                'transport': 'tcp:%d:interface=%s' % (int(qconfig['xmlrpc_port'] if qconfig['xmlrpc_port'] else 0),
                                                      qconfig['xmlrpc_ip']),
                'protocol': 'xmlrpc',
                'options': {'allow_none':True if qconfig['allow_none']=='True' else False},
            }
        if qconfig['rest_port']:
            config["transport_rest"] = {
                'transport': 'tcp:%d:interface=%s' % (int(qconfig['rest_port'] if qconfig['rest_port'] else 0),
                                                      qconfig['rest_ip']),
                'protocol': 'rest',
                'options': None,
            }
        if qconfig['amf_port']:
            config['transport_amf']={
                'transport': 'tcp:%d:interface=%s' % (int(qconfig['amf_port'] if qconfig['amf_port'] else 0),
                                                      qconfig['amf_ip']),
                'protocol': 'amf',
                'options': None,
                }

        # Don't do mail when no incoming server set
        if qconfig['mail_incoming_server']:
            config["transport_mail"] = {
                'protocol': 'mail',
                'options': {
                    'interval': int(qconfig['mail_check_interval'] if qconfig['mail_check_interval'] else 0),
                    'protocol': qconfig['mail_incoming_protocol'],
                    'address': qconfig['mail_from_address'],

                    'incoming_account': {
                        'server': qconfig['mail_incoming_server'],
                        'username': qconfig['mail_incoming_username'],
                        'password': qconfig['mail_incoming_password'],
                        'ssl': (qconfig['mail_incoming_ssl'].lower() == "true")
                    },

                    'outgoing_account': {
                        'server': qconfig['mail_outgoing_server'],
                        'username': qconfig['mail_outgoing_username'],
                        'password': qconfig['mail_outgoing_password'],
                        'ssl': (qconfig['mail_outgoing_ssl'].lower() == "true")
                    },
                }
            }

        services = q.config.getConfig('applicationserverservice')
        for servicename, serviceconfig in services.iteritems():
            config['service_%s' % servicename] = {
                'class': service_to_path(serviceconfig['classspec']),
                'options': None,
            }

        #Add manhole if configured through env
        if 'APPLICATIONSERVER_MANHOLE' in os.environ:
            transport, username, password = \
                os.environ['APPLICATIONSERVER_MANHOLE'].rsplit(':', 2)

            if 'transport_manhole' in config:
                raise RuntimeError('\'manhole\' transport already defined')

            config['transport_manhole'] = {
                'transport': transport,
                'protocol': 'ssh',
                'options': {
                    'user': username,
                    'password': password,
                },
            }

        return config


class FakeConfigReader:
    '''Fake configuration reader

    This reader returns a static dictionary containing hard-coded configuration
    data.
    '''
    implements(IConfigReader)

    def parseConfig(self):
        import os.path
        import inspect

        import applicationserver.example
        example_base = os.path.dirname(inspect.getabsfile(
            applicationserver.example))
        example = lambda e: os.path.join(example_base, e)

        ret = {
            'transport_xmlrpc':
                {
                    #This is a string representation of a "port" in Twisted
                    #See the documentation on twisted.application.strports for
                    #more info and samples
                    'transport': 'tcp:8000',
                    'protocol': 'xmlrpc',
                    'options': None,
                },
            'transport_rest':
                {
                    'transport': 'tcp:8001',
                    'protocol': 'rest',
                    'options': None,
                },
            'transport_manhole':
                {
                    'transport': 'tcp:8022',
                    'protocol': 'ssh',
                    'options': {
                        'user': 'admin',
                        'password': 'admin',
                    },
                },
            'service_test':
                {
                    'class': example('services.py:HelloService'),
                    'options': {
                        'greeting': 'Hello',
                    },
                },
            'service_cave':
                {
                    'class': example('services.py:SecretService'),
                    'options': None,
                },
            'service_request':
                {
                    'class': example('services.py:RequestService'),
                    'options': None,
                },
            'service_counter':
                {
                    'class': example('services.py:CounterService'),
                    'options': None,
                },
        }

        try:
            from pylabs import q
        except ImportError:
            pass
        else:
            ret['service_pmplatform'] = {
                    'class': example('pylabs_service.py:PMService'),
                    'options': None,
                }

        return ret
