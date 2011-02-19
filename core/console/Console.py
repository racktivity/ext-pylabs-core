from pylabs.Shell import *
import re
import sys
import pylabs
from pylabs.logging.RedirectStreams import isRedirected
from pylabs.pmtypes import IPv4Address, IPv4Range
import textwrap


IPREGEX = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

class Console:
    """
    class which groups functionality to print to a console 
    self.width=120
    self.indent=0 #current indentation of messages send to console
    self.reformat=False #if True will make sure message fits nicely on screen    
    """
    def __init__(self):
        self.width=120
        self.indent=0 #current indentation of messages send to console

    def rawInputPerChar(self,callback,params):
        """
        when typing, char per char will be returned
        """
        pylabs.q.platform.ubuntu.check()
        import termios, fcntl, sys, os
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    
        cont=True
        try:
            while cont:
                try:
                    c = sys.stdin.read(1)
                    cont,result,params=callback(c,params)
                except IOError: pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return cont,result,params

    
    def _cleanline(self,line):
        """
        make sure is string
        """
        try:
            line=str(line)
        except:
            raise ValueError("Could not convert text to string in system class.")
        return line

    def formatMessage(self,message,prefix="",withStar=False,indent=0,width=0):
        '''
        Reformat the message to display to the user and calculate length
        @param withStar means put * in front of message
        @returns: Length of last line and message to display
        @rtype: tuple<number, string>
        '''
        
        if indent==0 or indent==None:
            indent=self.indent
            
        #if pylabs.q.transaction.hasRunningTransactions():
        #    maxLengthStatusType= 8 #nr chars
        #else:
        #    maxLengthStatusType=0
            
        if prefix<>"":
            prefix="%s: "%(prefix)

        if withStar:
            prefix = '%s* %s' % (' ' * indent,prefix)
        else:
            prefix = ' %s%s' % (' ' * indent,prefix)
            
        if width==0:
            width=self.width
        maxMessageLength = width  -len(prefix) #- maxLengthStatusType
        if maxMessageLength<5:
            raise RuntimeError("Cannot format message for screen, not enough width\nwidht:%s prefixwidth:%s maxlengthstatustype:%s" % (width,len(prefix),maxMessageLength))
        
        #wrap the lines to fit on screen
        def reformat(line):
            if len(line)>0:
                endlf=line[-1]=="\n"
            else:
                endlf=False
            if len(line)>maxMessageLength:
                line=string.join(textwrap.wrap(line,maxMessageLength),"\n")
                if endlf:
                    line=line+"\n"
            return line
        lines=message.split("\n")                
        lines=[reformat(line) for line in lines]
        #ipshell()
        linesstr=string.join(lines,"\n")
        lines=linesstr.split("\n")
        
        indent=len(prefix)
        lines[0]="%s%s"%(prefix,lines[0])
        for linenr in range(1,len(lines)):
            lines[linenr]= '%s%s' % (' ' * indent,lines[linenr])
        return string.join(lines,"\n")
    
    
    def echo(self, msg,indent=None,withStar=False,prefix="",log=True,lf=True):
        '''
        Display some text to the end-user, use this method instead of print
        @param indent std, will use indent from console object (same for all), this param allows to overrule
                will only work when q.console.reformat==True

        '''
        msg=str(msg)
        if lf and msg<>"" and msg[-1]<>"\n":
            msg+="\n"
        msg=self._cleanline(msg)
        #if pylabs.q.transaction.hasRunningTransactions() and withStar==False:
        #    indent=self.indent+1
        msg=self.formatMessage(msg,indent=indent,withStar=withStar,prefix=prefix).rstrip(" ")
        pylabs.q.logger.inlog=True
        print msg,
        pylabs.q.logger.inlog=False
        if log:
            pylabs.q.logger.log(msg,1,dontprint=True)

    def echoListItem(self, msg):
        """
        Echo a list item
        @param msg: Message to display
        """
        self.echo(msg,withStar=True)

    def echoListItems(self, messages, sort=False):
        """
        Echo a sequence (iterator, generator, list, set) as list items

        @param messages: messages that need to be written to the console as list items
        @type messages: iterable
        @param sort: sort the messages before echoing them
        @type sort: bool
        @param loglevel: Log level
        @type loglevel: number
        """
        if sort:
            messages.sort()
        for msg in messages:
            self.echoListItem(msg)
            
    def echoWithPrefix(self,message,prefix,withStar=False,indent=None):
        """
        print a message which is formatted with a prefix
        """
        self.echo(message,prefix=prefix,withStar=withStar,indent=indent)

    def echoListWithPrefix(self,messages,prefix):
        """
        print messages
        """
        for message in messages:
            self.echoWithPrefix(message,prefix,withStar=True)
        
    def echoDict(self,dictionary,withStar=False,indent=None):
        for key in dictionary.keys():
            try:
                self.echoWithPrefix(str(dictionary[key]),key,withStar,indent)
            except:
                t,v,tb = sys.exc_info()
                q.eventhandler.logTryExcept(t,v,tb)                  
                raise RuntimeError("Could not convert item of dictionary %s to string" % key)

    def transformDictToMessage(self,dictionary,withStar=False,indent=None):
        for key in dictionary.keys():
            try:
                self.formatMessage(str(dictionary[key]),key,withStar,indent)
            except:
                t,v,tb = sys.exc_info()
                q.eventhandler.logTryExcept(t,v,tb)                  
                raise RuntimeError("Could not convert item of dictionary %s to string" % key)            

    def askString(self, question, defaultparam='', regex=None, retry=-1, validate=None):
        """Get a string response on a question

        @param question: Question to respond to
        @param defaultparam: Default response on the question if response not passed
        @param regex: Regex to match in the response
        @param retry: Integer counter to retry ask for respone on the question
        @param validate: Function to validate provided value

        @returns: Response provided by the user
        @rtype: string
        """
        if pylabs.q.qshellconfig.interactive<>True:
            raise RuntimeError ("Cannot ask a string in a non interactive mode.")
        if validate and not callable(validate):
            raise TypeError('The validate argument should be a callable')
        response = ""
        if not defaultparam == "" and defaultparam:
            question += " [%s]"%defaultparam
        question += ": "
        retryCount = retry
        while retryCount != 0:
            response = raw_input(question).rstrip()
            if response == "" and not defaultparam == "" and defaultparam:
                return defaultparam
            if (not regex or re.match(regex,response)) and (not validate or validate(response)):
                return response
            else:
                self.echo( "Please insert a valid value!")
                retryCount = retryCount - 1
        raise ValueError("Console.askString() failed: tried %d times but user didn't fill out a value that matches '%s'." % (retry, regex))

    def askPassword(self, question, confirm=True, regex=None, retry=-1, validate=None):
        """Present a password input question to the user

        @param question: Password prompt message
        @param confirm: Ask to confirm the password
        @type confirm: bool
        @param regex: Regex to match in the response
        @param retry: Integer counter to retry ask for respone on the question
        @param validate: Function to validate provided value

        @returns: Password provided by the user
        @rtype: string
        """
        if pylabs.q.qshellconfig.interactive<>True:
            raise RuntimeError ("Cannot ask a password in a non interactive mode."        )
        if validate and not callable(validate):
            raise TypeError('The validate argument should be a callable')
        response = ""
        import getpass
        startquestion = question
        if question.endswith(': '):
            question = question[:-2]
        question += ": "
        value=None
        failed = True
        retryCount = retry
        while retryCount != 0:
            response = getpass.getpass(question)
            if (not regex or re.match(regex,response)) and (not validate or validate(response)):
                if value == response or not confirm:
                    return response
                elif not value:
                    failed = False
                    value=response
                    question = "%s (confirm): " %(startquestion)
                else:
                    value=None
                    failed = True
                    question = "%s: "%(startquestion)
            if failed:
                self.echo("Invalid password!")
                retryCount = retryCount - 1
        raise RuntimeError(("Console.askPassword() failed: tried %s times but user didn't fill out a value that matches '%s'." % (retry, regex)))


    def askInteger(self, question, defaultValue = None, minValue = None, maxValue = None, retry = -1, validate=None):
        """Get an integer response on asked question

        @param question: Question need to get response on
        @param defaultparam: default response on the question if response not passed
        @param minValue: minimum accepted value for that integer
        @param maxValue: maximum accepted value for that integer
        @param retry: int counter to retry ask for respone on the question
        @param validate: Function to validate provided value

        @return: integer representing the response on the question
        """
        if pylabs.q.qshellconfig.interactive<>True:
            raise RuntimeError ("Cannot ask an integer in a non interactive mode.")
        if validate and not callable(validate):
            raise TypeError('The validate argument should be a callable')
        if not minValue == None and not maxValue == None:
            question += " (%d-%d)" % (minValue, maxValue)
        elif not minValue == None:
            question += " (min. %d)" % minValue
        elif not maxValue == None:
            question += " (max. %d)" % maxValue

        if not defaultValue == None:
            question += " [%d]" % defaultValue
        question += ": "

        retryCount = retry

        while retryCount != 0:
            response = raw_input(question).rstrip(chr(13))
            if response == "" and not defaultValue == None:
                return defaultValue
            if (re.match("^-?[0-9]+$",response.strip())) and (not validate or validate(response)):
                responseInt = int(response.strip())
                if (minValue == None or responseInt >= minValue) and (maxValue == None or responseInt <= maxValue):
                    return responseInt
            pylabs.q.console.echo("Please insert a valid value!")
            retryCount = retryCount - 1

        raise ValueError("Console.askInteger() failed: tried %d times but user didn't fill out a value that matches '%s'." % (retry, response))


    def askYesNo(self, message=""):
        '''Display a yes/no question and loop until a valid answer is entered

        @param message: Question message
        @type message: string

        @return: Positive or negative answer
        @rtype: bool
        '''
        if pylabs.q.qshellconfig.interactive<>True:
            raise RuntimeError ("Cannot ask a yes/no question in a non interactive mode.")
        
        while True:
            result = raw_input(str(message) + " (y/n):").rstrip(chr(13))
            if result.lower() == 'y' or result.lower() == 'yes':
                return True
            if result.lower() == 'n' or result.lower() == 'no':
                return False
            self.echo( "Illegal value. Press 'y' or 'n'.")
            
        
    def askIntegers(self, question, invalid_message="invalid input please try again.", min=None, max=None):
        """
        Ask the user for multiple integers

        @param question: question that will be echoed before the user needs to input integers
        @type question: string
        @param invalid_message: message that will be echoed when the user inputs a faulty value
        @type invalid_message: string
        @param min: optional minimal value for input values, all returned values will be at least min
        @type min: number or None
        @param max: optional maximal value for input values, all returned values will be at least max
        @type max: number of None
        @return: the input numbers
        @rtype: list<number>
        """
        def f():
            s = self.askString(question)
            return s.split(",")

        def clean(l):
            try:
                return [int(i.strip()) for i in l if i.strip() != ""]
            except ValueError, ex:
                return list()

        def all_between(l, min, max):
            for i in l:
                if (not min is None) and i < min:
                    return False
                elif (not max is None) and i > max:
                    return False
            return True

        def invalid(l):
            return len(l) == 0 or (not all_between(l, min, max))

        parts = clean(f())
        while invalid(parts):
            self.echo(invalid_message)
            parts = clean(f())
        return parts

    def askChoice(self,choicearray, descr=None, sort=False):
        #choicearray=["aabbccdd","aaddccaa","1","2","3","4","5","kristof","kristof3","kristof5","10","11","12","13","14","15","16"]
        maxchoice=20
        
        if len(choicearray)>maxchoice and pylabs.q.platform.isLinux():
            descr2 = "%s\nMake a selection please, start typing, we will try to do auto completion.\n     ? prints the list, * turns on wildcard search." % descr
            self.echo(descr2)
            print
            print "        ",
            if sort:
                choicearray.sort()
            wildcard=False
            chars=""
            params=[wildcard,chars]
            def process(char,params):
                """
                char per char will be returned from console
                """
                [wildcard,chars]=params
                #print (char,"","")
                sys.stdout.write(char)
                if char=="*":
                    params=[True,chars] #set wildcard
                    return True,[],params
                else:
                    chars="%s%s" %(chars,char)
                result=[]
                for choice in choicearray:
                    choice=str(choice)
                    choice=choice.lower()
                    if wildcard and choice.find(chars)<>-1:
                        result.append(choice)                    
                    #print "%s %s %s %s" % (wildcard,choice,chars,choice.find(chars))
                    if not wildcard and choice.find(chars)==0:
                        result.append(choice)
                    if char=="?":
                        return False,["99999"],params
                params=[wildcard,chars] 
                #print str(len(result)) + " " + chars + " " + str(wildcard)
                if len(result)<maxchoice and len(result)>0:
                    #more than 1 result but not too many to show and ask choice with nr's
                    return False,result,params
                return True,result,params

            if len(choicearray)==0:
                raise RuntimeError("Could not find choice with input %s" % chars)
            choicearray2=[]
            while len(choicearray2)==0:
                cont,choicearray2,params = self.rawInputPerChar(process,params)
                if len(choicearray2)==0:
                    self.echo("No results start over please")
                    print "        ",
                    wildcard=False
                    chars=""
                    params=[wildcard,chars]

            if len(choicearray2)==1 and not choicearray2==["99999"]:
                sys.stdout.write(choicearray2[0][len(chars):])
            if choicearray2==["99999"]:
                self.echo("\n")
                for choice in choicearray:
                    choice=str(choice)                    
                    self.echoListItem(choice)                    
                self.echo("\n")
                return self.askChoice(choicearray, descr, sort)            
            else:
                return self._askChoice(choicearray2, descr, sort)            
        else:
            return self._askChoice(choicearray, descr, sort)
            

    def _askChoice(self, choicearray, descr=None, sort=False):
        if pylabs.q.qshellconfig.interactive<>True:
            raise RuntimeError ("Cannot ask a choice in an list of items in a non interactive mode.")
        if not choicearray:
            return None
        if len(choicearray) == 1:
            self.echo("Found exactly one choice: %s"%(choicearray[0]))
            return choicearray[0]
        descr = descr or "\nMake a selection please: "
        if sort:
            choicearray.sort()

        self.echo(descr)

        nr=0
        for section in choicearray:
            nr=nr+1
            self.echo("   %s: %s" % (nr, section))
        self.echo("")
        result = self.askInteger("   Select Nr", minValue = 1, maxValue = nr)
        
        return choicearray[result-1]

    def askChoiceMultiple(self, choicearray, descr=None, sort=None):
        if pylabs.q.qshellconfig.interactive<>True:
            raise RuntimeError ("Cannot ask a choice in an list of items in a non interactive mode.")
        if not choicearray:
            return []
        if len(choicearray) == 1:
            self.echo("Found exactly one choice: %s"%(choicearray[0]))
            return choicearray
        descr = descr or "\nMake a selection please: "
        if sort:
            choicearray.sort()

        self.echo(descr)

        nr=0
        for section in choicearray:
            nr=nr+1
            self.echo("   %s: %s" % (nr, section))
        self.echo("")
        results = self.askIntegers("   Select Nr, use comma separation if more e.g. \"1,4\"",
                                   "Invalid choice, please try again",
                                   min=1,
                                   max=len(choicearray))
        return [choicearray[i-1] for i in results]

    def askMultiline(self, question, escapeString='.'):
        """
        Ask the user a question that needs a multi-line answer.

        @param question: The question that should be asked to the user
        @type question: string
        @param escapeString: Optional custom escape string that is used by the user to indicate input has ended.
        @type escapeString: string
        @return: string multi-line reply by the user, always ending with a newline
        """
        self.echo("%s:" % question)
        self.echo("(Enter answer over multiple lines, end by typing '%s' (without the quotes) on an empty line)" % escapeString)
        lines = []
        user_input = raw_input()
        while user_input != escapeString:
            lines.append(user_input)
            user_input = raw_input()
        lines.append("") # Forces end with newline
        return '\n'.join(lines)
    
    def askIpaddressInRange(self, question, startip=None, endip=None, network=None, netmask=None, retry=-1):
        """
        Ask the user to enter a valid ipaddress
        
        Provide either startip and endip or network and netmask.
        
        @param question: The question that should be asked to the user
        @type question: string
        @param startip: Start ip of the available ip range to enter the ipaddress in
        @type startip: string
        @param endip: End ip of the available ip range to enter the ipaddress in
        @type endip: string
        @param network: Base IP address when using netmask-based range definition
        @type network: string
        @param netmask: Netmask to use in combination with C{network}
        @type netmask: string
        @return: Ip address
        @rtype: string

        """
        def _askIpaddress(question, startip=None, endip=None, network=None, netmask=None):
            if startip and endip:
                return self.askString('%s(Range %s - %s)'%(question, startip, endip), regex=IPREGEX)
            if network and netmask:
                iprange = IPv4Range(netIp=network, netMask=netmask)
                return self.askString('%s(Range %s - %s)'%(question, str(iprange.fromIp), str(iprange.toIp)), regex=IPREGEX)

        if (startip or endip) and (network or netmask):
            raise ValueError("Provide either startip and endip or networkip and netmask")
        if (startip or endip) and not (startip and endip):
            raise ValueError("Provide either startip and endip or networkip and netmask")
        if (network or netmask) and not (network and netmask):
            raise ValueError("Provide either startip and endip or network and netmask")
        if (network and netmask) and (IPv4Address(int(IPv4Address(network)) & int(IPv4Address(netmask))) != network):
            raise ValueError("Provided network and netmask don't match")

        retryCount = retry
        while retryCount != 0:
            ipaddress = _askIpaddress(question, startip, endip, network, netmask)
            iprange = IPv4Range(fromIp=startip, toIp=endip, netIp=network, netMask=netmask)
            if ipaddress in IPv4Range(fromIp=startip, toIp=endip, netIp=network, netMask=netmask):
                return ipaddress
            self.echo( "The provided ipaddress not in range, please try again")
            retryCount = retryCount - 1
            
    def showOutput(self):
        pass
        
    def hideOutput(self):
        pass        