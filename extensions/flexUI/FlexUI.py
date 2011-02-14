from pymonkey import *
from pymonkey.Shell import *
import simplejson
from threading import Thread

#Copyright Jon Berg , turtlemeat.com

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from WizardActions  import WizardActions
#import pri

def testWizardFunction(server):
    """ Create a simple form and print the result """
    form = q.gui.form.createForm()
    tab1 = form.addTab('general','General')
    tab1.message('msg1','Snapshot Multiple Machines', True, False)
    return server.askForm(form)
    
class Object():
    pass

class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        result = form["result"].value
        
        objResult = self.process(self.path, simplejson.loads(result))
        print 'sending back: ' + objResult
        self.wfile.write(objResult)

    # gets an object as input and responds with an object as output
    def process(self, path, resultObj):
        #print  'Path: '  + path
        #print  'Result:' + resultObj['text']
        # obj = {'text':'passed'}
        # return obj
        return testWizardFunction(FlexUI())

class FlexUI:

    def launchServer(self):
        server = HTTPServer(('', 80), MyHandler)
        print "starting server..."
        server.serve_forever()

    def launchBrowser(self):
        "Launches the browser that directly connects to the server"
        url = 'file:///opt/qbase3/lib/pymonkey/extensions/flexUI/flexapp/bin/Wizard.html'
        q.system.process.execute("firefox '%s'" % (url))

    def launch(self, wizardFunction):
        """ from a tasklet """
        pass

    def _isMap(self, data):
        return type(data) == type({})

    def _isList(self, data):
        return type(data) == type([])

    def prettyPrintJSON(self, data, level=0):
        res = ''
        if self._isMap(data):
            for key, value in data.items():
                if self._isMap(value):
                    res += ' ' * level + key + ':' + '\n'
                    res += self.prettyPrintJSON(value, level + 4)
                elif self._isList(value):
                    res += ' ' * level + key + ':' + '\n'
                    res += self.prettyPrintJSON(value, level + 4)
                else:
                    res += ' ' * level + key + ':' + str(value) + '\n'
        elif self._isList(data):
            for i in range(len(data)):
                el = data[i]
                if self._isMap(el):
                    res += ' ' * level + '[%s]:' % i + '\n'
                    res += self.prettyPrintJSON(el, level + 4)
                elif self._isList(value):
                    res += ' ' * level + '[%s]:' % i + '\n'
                    res += self.prettyPrintJSON(value, level + 4)
                else:
                    res += ' ' * level + key + ':' + str(value) + '\n'
        else:
            res += str(data) + '\n'
        return res

    def askForm(self, form):
        a    = WizardActions()
        data = a.Form(form)
        return '{"action":"display", "params": {"control": "label", "text": "Snapshot Multiple Machines", "multiline": false, "name": "msg1", "bold": true}}'
        #print self.prettyPrintJSON(simplejson.loads(data))
        #return data

        #
        # print self.prettyPrintJSON(data)

    def doTest(self):
        testWizardFunction(self)

    def doHelloWorld(self):
        tmp = self
        class MyThread(Thread):
            def run(self):
                tmp.launchServer()
        th = MyThread()
        th.start()
        self.launchBrowser()

