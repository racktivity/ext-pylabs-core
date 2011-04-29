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

import time
import socket
import re

import pylabs

class SystemNet:

    def __init__(self):
        self._windowsNetworkInfo = None

    def getNameServer(self):
        """Returns the first nameserver IP found in /etc/resolv.conf

        Only implemented for Unix based hosts.

        @returns: Nameserver IP
        @rtype: string

        @raise NotImplementedError: Non-Unix systems
        @raise RuntimeError: No nameserver could be found in /etc/resolv.conf
        """
        if not pylabs.q.platform.isUnix():
            raise NotImplementedError(
                'This function is only supported on Unix systems')

        nameserverlines = pylabs.q.codetools.regex.findAll(
            "^\s*nameserver\s+(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s*$",
            pylabs.q.system.fs.fileGetContents('/etc/resolv.conf')
        )

        if not nameserverlines:
            raise RuntimeError('No nameserver found in /etc/resolv.conf')

        nameserverline = nameserverlines[0]

        return nameserverline.strip().split(' ')[-1]

    def getIpAdresses(self,up=False):
        nics=self.getNics(up)
        result=[]
        for nic in nics:
            ipTuple = self.getIpAddress(nic)
            if ipTuple: # if empty array skip
                result.append(ipTuple[0][0])
        return result
    
    def checkIpAddressIsLocal(self,ipaddr):
        if ipaddr.strip() in self.getIpAdresses():
            return True
        else:
            return False

    def enableProxy(self):
        maincfg = pylabs.q.config.getConfig('main')
        if 'proxy' in maincfg:
            import os, urllib2
            proxycfg = maincfg['proxy']
            proxyserver = proxycfg['server']
            params = ""
            proxyuser =  proxycfg.get('user')
            if proxyuser:
                params += proxyuser
                proxypassword = proxycfg.get('password')
                if proxypassword:
                    params += ":%s" % proxypassword
                params += "@"
            params += proxyserver
            if pymonkey.q.platform.isUnix():
                os.environ['http_proxy'] = proxyserver
            proxy_support = urllib2.ProxyHandler()
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)
    
    def getNics(self,up=False):
        """ Get Nics on this machine
        Works only for Linux/Solaris systems
        @param up: only returning nics which or up
        """
        niclist = []
        regex = ''
        output = ''
        if pylabs.q.platform.isLinux() or pylabs.q.platform.isESX():
            exitcode,output = pylabs.q.system.process.execute("ip l", outputToStdout=False)
            if not up:
                regex = "^\d+:\s(?P<name>[\w\d]*):.*$"
            else:
                regex = "^\d+:\s(?P<name>[\w\d]*):\s<.*UP.*>.*$"
            return list(set(re.findall(regex,output,re.MULTILINE)))
        elif pylabs.q.platform.isSolaris():
            exitcode,output = pylabs.q.system.process.execute("ifconfig -a", outputToStdout=False)
            if up:
                regex = "^([\w:]+):\sflag.*<.*UP.*>.*$"
            else:
                regex = "^([\w:]+):\sflag.*$"
            nics = set(re.findall(regex,output,re.MULTILINE))
            exitcode,output = pylabs.q.system.process.execute("dladm show-phys", outputToStdout=False)
            lines = output.splitlines()
            for line in lines[1:]:
                nic = line.split()
                if up:
                    if nic[2] == 'up':
                        nics.add(nic[0])
                else:
                    nics.add(nic[0])
            return list(nics)
        else:
            raise RuntimeError("Not supported on this platform!")

    def getNicType(self,interface):
        """ Get Nic Type on a certain interface
        @param interface: Interface to determine Nic type on

        @raise RuntimeError: On linux if ethtool is not present on the system
        """
        if pylabs.q.platform.isLinux() or pylabs.q.platform.isESX():
            output=''
            if pylabs.q.system.fs.exists("/sys/class/net/%s"%interface):
                output = pylabs.q.system.fs.fileGetContents("/sys/class/net/%s/type"%interface)
            if output.strip() == "32":
                return "INFINIBAND"
            else:
                if pylabs.q.system.fs.exists('/proc/net/vlan/%s'%(interface)):
                    return 'VLAN'
                exitcode,output = pylabs.q.system.process.execute("which ethtool", False, outputToStdout=False)
                if exitcode != 0:
                    raise RuntimeError("Ethtool is not installed on this system!")
                exitcode,output = pylabs.q.system.process.execute("ethtool -i %s"%(interface),False,outputToStdout=False)
                if exitcode !=0:
                    return 'VIRTUAL'
                match = re.search("^driver:\s+(?P<driver>\w+)\s*$",output,re.MULTILINE)
                if match and match.group("driver") == "tun" :
                    return "VIRTUAL"
                if match and match.group("driver") == "bridge" :
                    return "VLAN"
                return "ETHERNET_GB"
        elif pylabs.q.platform.isSolaris():
            command = "ifconfig %s"%interface
            exitcode,output = pylabs.q.system.process.execute(command, outputToStdout=False, dieOnNonZeroExitCode=False)
            if exitcode != 0:
                # temporary plumb the interface to lookup its mac
                pylabs.q.logger.log("Interface %s is down. Temporarily plumbing it to be able to lookup its nic type" % interface, 1)
                pylabs.q.system.process.execute('%s plumb' % command, outputToStdout=False)
                (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False)
                pylabs.q.system.process.execute('%s unplumb' % command, outputToStdout=False)
            if output.find("ipib") >=0:
                return "INFINIBAND"
            else:
                #work with interfaces which are subnetted on vlans eq e1000g5000:1
                interfacepieces = interface.split(':')
                interface = interfacepieces[0]
                match = re.search("^\w+?(?P<interfaceid>\d+)$",interface,re.MULTILINE)
                if not match:
                    raise ValueError("Invalid interface %s"%(interface))
                if len(match.group('interfaceid')) >= 4:
                    return "VLAN"
                else:
                    if len(interfacepieces) > 1:
                        return "VIRTUAL"
                    else:
                        return "ETHERNET_GB"
        else:
            raise RuntimeError("Not supported on this platform!")

    def getVlanTag(self,interface,nicType=None):
        """Get VLan tag on the specified interface and vlan type"""
        if nicType == None:
            nicType=pylabs.q.system.net.getNicType(interface)
        if nicType == "INFINIBAND" or nicType=="ETHERNET_GB" or nicType == "VIRTUAL":
            return "0"
        if pylabs.q.platform.isLinux():
            #check if its a vlan
            vlanfile = '/proc/net/vlan/%s'%(interface)
            if pylabs.q.system.fs.exists(vlanfile):
                return pylabs.q.system.net.getVlanTagFromInterface(interface)
            bridgefile = '/sys/class/net/%s/brif/'%(interface)
            for brif in pylabs.q.system.fs.listDirsInDir(bridgefile):
                brif = pylabs.q.system.fs.getBaseName(brif)
                vlanfile = '/proc/net/vlan/%s'%(brif)
                if pylabs.q.system.fs.exists(vlanfile):
                    return pylabs.q.system.net.getVlanTagFromInterface(brif)
            return "0"
        elif pylabs.q.platform.isSolaris():
            return pylabs.q.system.net.getVlanTagFromInterface(interface)
        else:
            raise RuntimeError("Not supported on this platform!")

    def getVlanTagFromInterface(self,interface):
        """Get vlan tag from interface
        @param interface: string interface to get vlan tag on
        @rtype: integer representing the vlan tag
        """
        if pylabs.q.platform.isLinux():
            vlanfile = '/proc/net/vlan/%s'%(interface)
            if pylabs.q.system.fs.exists(vlanfile):
                content = pylabs.q.system.fs.fileGetContents(vlanfile)
                match = re.search("^%s\s+VID:\s+(?P<vlantag>\d+)\s+.*$"%(interface),content,re.MULTILINE)
                if match:
                    return match.group('vlantag')
                else:
                    raise ValueError("Could not find vlantag for interface %s"%(interface))
            else:
                raise ValueError("This is not a vlaninterface %s"%(interface))
        elif pylabs.q.platform.isSolaris():
            #work with interfaces which are subnetted on vlans eq e1000g5000:1
            interface = interface.split(':')[0]
            match = re.search("^\w+?(?P<interfaceid>\d+)$",interface,re.MULTILINE)
            if not match:
                raise ValueError("This is not a vlaninterface %s"%(interface))
            return int(match.group('interfaceid'))/1000

    def getReachableIpAddress(self, ip, port):
        """Returns the first local ip address that can connect to the specified ip on the specified port"""
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((ip, port))
        except:
            raise RuntimeError("No ip foungetIpAddressd that can connect to %s:%s"%(ip,port))
        return s.getsockname()[0]

    def getIpAddress(self, interface):
        """Return a list of ip addresses and netmasks assigned to this interface"""
        if pylabs.q.platform.isLinux() or pylabs.q.platform.isESX():
            command = "ip a s %s" % interface
            (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False, dieOnNonZeroExitCode=False)
            if exitcode != 0:
                return []
            nicinfo = re.findall("^\s+inet\s+(.*)\/(\d+)\s(?:brd\s)?(\d+\.\d+\.\d+\.\d+)?\s?scope.*$",output,re.MULTILINE)
            result = []
            for ipinfo in nicinfo:
                ip = ipinfo[0]
                masknumber = int(ipinfo[1])
                broadcast = ipinfo[2]
                mask = ""
                for i in range(4):
                    mask += str(int(hex(pow(2,32)-pow(2,32-masknumber))[2:][i*2:i*2+2],16)) + "."
                result.append([ip, mask[:-1], broadcast])
            return result
        elif pylabs.q.platform.isSolaris():
            command = "ifconfig %s"%(interface)
            (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False, dieOnNonZeroExitCode=False)
            if exitcode != 0:
                return []
            result = []
            match = re.search("^\s+inet\s+(?P<ipaddress>[\d\.]+)\s+.*netmask\s+(?P<netmask>[a-f\d]{8})\s?(broadcast)?\s?(?P<broadcast>[\d\.]+)?$", output, re.MULTILINE)
            if not match:
                return []
            ip = match.group('ipaddress')
            netmaskhex = match.group('netmask')
            broadcast = match.group('broadcast')
            mask =""
            for j in range(4):
                mask += str(int(netmaskhex[j*2:j*2+2], 16)) + "."
            return [[ip , mask[:-1], broadcast]]
        else:
            raise RuntimeError("q.system.net.getIpAddress not supported on this platform")

    def getMacAddress(self, interface):
        """Return the MAC address of this interface"""
        if not interface in self.getNics():
            raise LookupError("Interface %s not found on the system" % interface)
        if pylabs.q.platform.isLinux() or pylabs.q.platform.isESX():
            if pylabs.q.system.fs.exists("/sys/class/net"):
                return pylabs.q.system.fs.fileGetContents('/sys/class/net/%s/address' % interface).strip()
            else:
                command = "ifconfig %s | grep HWaddr| awk '{print $5}'"% interface
                (exitcode,output)=pylabs.q.system.process.execute(command, outputToStdout=False)
                return self.pm_formatMacAddress(output)
        elif pylabs.q.platform.isSolaris():
            # check if interface is a logical inteface ex: bge0:1
            tokens = interface.split(':')
            if len(tokens) > 1 :
                interface = tokens[0]
            command = "ifconfig %s" % interface
            (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False, dieOnNonZeroExitCode=False)
            if exitcode != 0:
                # temporary plumb the interface to lookup its mac
                pylabs.q.logger.log("Interface %s is down. Temporarily plumbing it to be able to lookup its MAC address" % interface, 1)
                pylabs.q.system.process.execute('%s plumb' % command, outputToStdout=False)
                (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False, dieOnNonZeroExitCode=False)
                pylabs.q.system.process.execute('%s unplumb' % command, outputToStdout=False)
            if exitcode == 0:
                match = re.search(r"^\s*(ipib|ether)\s*(?P<mac>\S*)", output, re.MULTILINE)
                if match:
                    return self.pm_formatMacAddress(match.group("mac"))
            return None
        else:
            raise RuntimeError("q.system.net.getMacAddress not supported on this platform")

    def pm_formatMacAddress(self, macaddress):
        macpieces = macaddress.strip().split(':')
        mac = ""
        for piece in macpieces:
            if len(piece)==1:
                mac += "0"
            mac += piece + ":"
        mac = mac[:-1]
        return mac

    def isIpInDifferentNetwork(self, ipaddress):
        for nic in pylabs.q.system.net.getNics():
            for ip in pylabs.q.system.net.getIpAddress(nic):
                if pylabs.pmtypes.IPv4Address(ipaddress) in pylabs.pmtypes.IPv4Range(netIp=ip[0], netMask=ip[1]):
                    return False
        return True

    def getMacAddressForIp(self, ipaddress):
        """Search the MAC address of the given IP address in the ARP table

        @param ipaddress: IP address of the machine
        @rtype: string
        @return: The MAC address corresponding with the given IP
        @raise: RuntimeError if no MAC found for IP or if platform is not suppported
        """
        def doArp(ipaddress):
            args = list()
            if pylabs.q.platform.isLinux():
                # We do not want hostnames to show up in the ARP output
                args.append("-n")

            return pylabs.q.system.process.execute(
                'arp %s %s' % (" ".join(args), ipaddress),
                dieOnNonZeroExitCode=False,
                outputToStdout=False
            )

        def noEntry(output):
            return ("no entry" in output) or ("(incomplete)" in output)

        if pylabs.q.platform.isUnix():
            if self.isIpInDifferentNetwork(ipaddress):
                warning = 'The IP address %s is from a different subnet. This means that the macaddress will be the one of the gateway/router instead of the correct one.'
                pylabs.q.errorconditionhandler.raiseWarning(warning % ipaddress)

            exitcode, output = doArp(ipaddress)
            # Output of arp is 1 when no entry found is 1 on solaris but 0
            # on Linux, so we check the actual output
            if noEntry(output):
                # ping first and try again
                self.pingMachine(ipaddress, pingtimeout=1)
                exitcode, output = doArp(ipaddress)

            if not noEntry(output) and pylabs.q.platform.isSolaris():
                mac = output.split()[3]
                return self.pm_formatMacAddress(mac)
            else:
                mo = re.search("(?P<ip>[0-9]+(.[0-9]+){3})\s+(?P<type>[a-z]+)\s+(?P<mac>([a-fA-F0-9]{2}[:|\-]?){6})",output)
                if mo:
                    return self.pm_formatMacAddress(mo.groupdict()['mac'])
                else:
                    # On Linux the arp will not show local configured ip's in the table.
                    # That's why we try to find the ip with "ip a" and match for the mac there.

                    output, stdout, stderr = pylabs.q.system.process.run('ip a', stopOnError=False)
                    if exitcode:
                        raise RuntimeError('Could not get the MAC address for [%s] because "ip" is not found'%s)
                    mo = re.search('\d:\s+\w+:\s+.*\n\s+.+\s+(?P<mac>([a-fA-F0-9]{2}[:|\-]?){6}).+\n\s+inet\s%s[^0-9]+'%ipaddress, stdout, re.MULTILINE)
                    if mo:
                        return self.pm_formatMacAddress(mo.groupdict()['mac'])
            raise RuntimeError("MAC address for [%s] not found"%ipaddress)
        else:
            raise RuntimeError("q.system.net.getMacAddressForIp not supported on this platform")

    def getHostname(self):
        """Get hostname of the machine
        """
        return socket.gethostname()

    def isNicConnected(self,interface):
        if pylabs.q.platform.isLinux():
            carrierfile = '/sys/class/net/%s/carrier'%(interface)
            if not pylabs.q.system.fs.exists(carrierfile):
                return False
            try:
                return int(pylabs.q.system.fs.fileGetContents(carrierfile)) != 0
            except IOError:
                return False
        elif pylabs.q.platform.isESX():
            nl = pylabs.q.system.net.getNics(up=True)
            if interface not in nl:
                return False
            else:
                return True
        elif pylabs.q.platform.isSolaris():
            if pylabs.q.platform.getVersion() < 100:
                command = "dladm show-dev -p -o STATE %s" % interface
                expectResults = ['STATE="up"', 'STATE="unknown"']
            else:
                command = "dladm show-phys -p -o STATE %s" % interface
                expectResults = ['up', 'unknown']

            (exitcode, output) = pylabs.q.system.process.execute(command, dieOnNonZeroExitCode=False, outputToStdout=False)
            if exitcode != 0:
                return False
            output = output.strip()
            if output in expectResults:
                return True
            else:
                return False

    def getHostByName(self, dnsHostname):
        import socket
        return socket.gethostbyname(dnsHostname)
    def getDefaultRouter(self):
        """Get default router
        @rtype: string representing the router interface
        """
        if pylabs.q.platform.isLinux() or pylabs.q.platform.isESX():
            command = "ip r | grep 'default' | awk {'print $3'}"
            (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False)
            return output.strip()
        elif pylabs.q.platform.isSolaris():
            command = "netstat -rn | grep default | awk '{print $2}'"
            (exitcode, output) = pylabs.q.system.process.execute(command, outputToStdout=False)
            return output.strip()
        else:
            raise RuntimeError("q.system.net.getDefaultRouter not supported on this platform")

    def validateIpAddress(self, ipaddress):
        """Validate wether this ip address is a valid ip address of 4 octets ranging from 0 to 255 or not
        @param ipaddress: ip address to check on
        @rtype: boolean...True if this ip is valid, False if not
        """
        if len(ipaddress.split()) == 1:
            ipList = ipaddress.split('.')
            if len(ipList) == 4:
                for i, item in enumerate(ipList):
                    try:
                        ipList[i] = int(item)
                    except:
                        return False
                    if not isinstance(ipList[i], int):
                        pylabs.q.logger.log('[%s] is not a valid ip address, octects should be integers'%ipaddress, 7)
                        return False
                if max(ipList) < 256:
                    pylabs.q.logger.log('[%s] is a valid ip address'%ipaddress, 9)
                    return True
                else:
                    pylabs.q.logger.log('[%s] is not a valid ip address, octetcs should be less than 256'%ipaddress, 7)
                    return False
            else:
                pylabs.q.logger.log('[%s] is not a valid ip address, ip should contain 4 octets'%ipaddress, 7)
                return False
        else:
            pylabs.q.logger.log('[%s] is not a valid ip address'%ipaddress, 7)
            return False

    def pingMachine(self, ip, pingtimeout=60, recheck = False, allowhostname = False):
        """Ping a machine to check if it's up/running and accessible
        @param ip: Machine Ip Address
        @param pingtimeout: time in sec after which ip will be declared as unreachable
        @param recheck: Unused, kept for backwards compatibility
        @param allowhostname: allow pinging on hostname (default is false)
        @rtype: True if machine is pingable, False otherwise
        """
        if not allowhostname:
            if not pylabs.q.system.net.validateIpAddress(ip):
                raise ValueError('ERROR: invalid ip address passed:[%s]'%ip)

        pylabs.q.logger.log('pingMachine %s, timeout=%d, recheck=%s' % (ip, pingtimeout, str(recheck)), 8)

        start = time.time()
        pingsucceeded = False
        while time.time() - start < pingtimeout:
            if pylabs.q.platform.isSolaris():
                #ping -c 1 IP 1
                #Last 1 is timeout in seconds
                exitcode, output = pylabs.q.system.process.execute(
                                    'ping -c 1 %s 1' % ip, False, False)
            elif pylabs.q.platform.isLinux():
                #ping -c 1 -W 1 IP
                exitcode, output = pylabs.q.system.process.execute(
                                    'ping -c 1 -W 1 %s' % ip, False, False)
            elif pylabs.q.platform.isUnix():
                exitcode, output = pylabs.q.system.process.execute('ping -c 1 %s'%ip, False, False)
            elif pylabs.q.platform.isWindows():
                exitcode, output = pylabs.q.system.process.execute('ping -w %d %s'%(pingtimeout, ip), False, False)
            else:
                raise RuntimeError('Platform is not supported')
            if exitcode == 0:
                pingsucceeded = True
                pylabs.q.logger.log('Machine with ip:[%s] is pingable'%ip, 9)
                return True
            time.sleep(1)
        if not pingsucceeded:
            pylabs.q.logger.log("Could not ping machine with ip:[%s]"%ip, 7)
            return False


    def isIpInHostsFile(self, hostsfile, ip):
        """Check if ip is in the hostsfile
        @param hostsfile: File where hosts are defined
        @param ip: Ip of the machine to check
        """
        # get content of hostsfile
        filecontents = pylabs.q.system.fs.fileGetContents(hostsfile)
        res = re.search('^%s\s' %ip, filecontents, re.MULTILINE)
        if res:
            return True
        else:
            return False

    def removeFromHostsFile(self, hostsfile, ip):
        """Update a hostfile, delete ip from hostsfile
        @param hostsfile: File where hosts are defined
        @param ip: Ip of the machine to remove
        """
        pylabs.q.logger.log('Updating hosts file %s: Removing %s' % (hostsfile, ip), 8)
        # get content of hostsfile
        filecontents = pylabs.q.system.fs.fileGetContents(hostsfile)
        searchObj = re.search('^%s\s.*\n' %ip, filecontents, re.MULTILINE)
        if searchObj:
            filecontents = filecontents.replace(searchObj.group(0), '')
            pylabs.q.system.fs.writeFile(hostsfile, filecontents)
        else:
            pylabs.q.logger.log('Ip address %s not found in hosts file' %ip, 1)
            
    def getHostNamesForIP(self, hostsfile, ip):
        """Get hostnames for ip address
        @param hostsfile: File where hosts are defined
        @param ip: Ip of the machine to get hostnames from
        @return: List of machinehostnames
        """
        pylabs.q.logger.log('Get hostnames from hosts file %s for ip %s' % (hostsfile, ip), 8)
        # get content of hostsfile
        if self.isIpInHostsFile(hostsfile, ip):
            filecontents = pylabs.q.system.fs.fileGetContents(hostsfile)
            searchObj = re.search('^%s\s.*\n' %ip, filecontents, re.MULTILINE)
            hostnames = searchObj.group(0).strip().split()
            hostnames.pop(0)
            return hostnames
        else:
            return []

    def updateHostsFile(self,hostsfile,ip,hostname):
        """Update a hostfile to contain the basic information install
        @param hostsfile: File where hosts are defined
        @param ip: Ip of the machine to add/modify
        @param hostname: List of machinehostnames to add/modify
        """
        if isinstance(hostname, str):
            hostname = hostname.split()
        pylabs.q.logger.log('Updating hosts file %s: %s -> %s' % (hostsfile, hostname, ip), 8)
        # get content of hostsfile
        filecontents = pylabs.q.system.fs.fileGetContents(hostsfile)
        searchObj = re.search('^%s\s.*\n' %ip, filecontents, re.MULTILINE)
        
        hostnames = ' '.join(hostname)
        if searchObj:
            filecontents = filecontents.replace(searchObj.group(0), '%s %s\n' %(ip, hostnames))
        else:
            filecontents += '%s %s\n' %(ip, hostnames)

        pylabs.q.system.fs.writeFile(hostsfile, filecontents)


    def download(self, url, localpath, username=None, passwd=None):
        '''Download a url to a file or a directory, supported protocols: http, https, ftp, file
        @param url: URL to download from
        @type url: string
        @param localpath: filename or directory to download the url to
        @type localpath: string
        @param username: username for the url if it requires authentication
        @type username: string
        @param passwd: password for the url if it requires authentication
        @type passwd: string
        '''
        if not url:
            raise ValueError('URL can not be None or empty string')
        if not localpath:
            raise ValueError('Local path to download the url to can not be None or empty string')
        filename = ''
        if pylabs.q.system.fs.isDir(localpath):
            filename = pylabs.q.system.fs.joinPaths(localpath, pylabs.q.system.fs.getBaseName(url))
        else:
            if pylabs.q.system.fs.isDir(pylabs.q.system.fs.getDirName(localpath)) and not pylabs.q.system.fs.exists(localpath):
                filename = localpath
            else:
                raise ValueError('Local path is an invalid path')
        pylabs.q.logger.log('Downloading url %s to local path %s'%(url, filename), 4)

        from urllib import FancyURLopener, splittype
        class myURLOpener(FancyURLopener):
            # read a URL, with automatic HTTP authentication
            def __init__(self, user, passwd):
                self._user = user
                self._passwd = passwd
                self._promptcalled = False
                FancyURLopener.__init__(self)

            def prompt_user_passwd(self, host, realm):
                if not self._user or not self._passwd:
                    raise RuntimeError('Server requested authentication but nothing was given')
                if not self._promptcalled:
                    self._promptcalled = True
                    return self._user, self._passwd
                raise RuntimeError('Could not authenticate with the given authentication user:%s and password:%s'%(self._user, self._passwd))

        urlopener = myURLOpener(username, passwd)
        if username and passwd and splittype(url)[0] == 'ftp':
            url = url.split('://')[0]+'://%s:%s@'%(username,passwd)+url.split('://')[1]
        urlopener.retrieve(url, filename, None, None)
        pylabs.q.logger.log('URL %s is downloaded to local path %s'%(url, filename), 4)

    def getDomainName(self):
        """
        Retrieve the dns domain name
        """
        cmd= "dnsdomainname" if pylabs.q.platform.isLinux() else "domainname" if pylabs.q.platform.isSolaris() else ""
        if not cmd:
            raise PlatformNotSupportedError('Platform "%s" is not supported. Command is only supported on Linux and Solaris'%pylabs.q.platform.name)

        exitCode, domainName=pylabs.q.system.process.execute(cmd, outputToStdout=False)
        domainName = domainName.splitlines()[0]

        if not domainName:
            raise ValueError('Failed to retrieve domain name')

        return domainName

class PlatformNotSupportedError(RuntimeError): pass

class NetworkZone:
    ipRanges=None ##array(IPRange)
