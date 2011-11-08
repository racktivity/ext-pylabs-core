@metadata title=Execute Remote Scripts
@metadata tagstring=remote script execute

# How to  Execute Scripts on a Remote Server using the Pylabs Framework

[[warning]]
**Warning**

This information is outdated.
[[/warning]]

## Installing `qshell_remote`

To enable remote execution over ssh you require to install the qpackage qshell_remote
[[code]]
In [1]: i.qpackages.find('remote*')
Found exactly one choice: qshell_remote 1.0 (pylabs.org) - SERVER
 
In [2]: i.qpackages.lastQPackages.qshell_remote.install()
 * Downloading QPackage qshell_remote                        DONE
 * Installing QPackage qshell_remote                         RUNNING
 *  Executing Install Tasklet of QPackage qshell_remote      DONE
 * Installing QPackage qshell_remote                         FINISHED

In [3]: 
[[/code]]

This will enable an extra extension on the q. tree available as:

[[code]]
In [4]: q.clients.ssh.createClient(?
Definition: q.clients.ssh.createClient(self, host, username, password, timeout)
Documentation:
    Create a new SSHClient instance.
    
    
    Parameters:
    
    - host: Hostname to connect to
    - username: Username to connect as
    - password: Password to authenticate with
    - timeout: Connection timeout
    
    Returns: SSHClient instance
[[/code]]


## Creating a Client for a Remote Connection

To access a remote system over ssh, you need to create a client connection first:

[[code]]
In [7]: host = '192.168.11.162'

In [8]: login = 'root'

In [9]: password = 'rooter'

In [10]: timeout = 30

In [11]: client = q.clients.ssh.createClient(host, login, password, timeout)
[[/code]]

This will create a connection object providing you with some methods to execute scripts on the remote system:

[[code]]
In [12]: client.
client.client         client.getOutPut(     client.logSSHToFile(  client.timeout        
client.execute(       client.host           client.password       client.username      
[[/code]]


## Executing a Remote Script

Here is a little sample where I try to get the remote system's kernel info:

[[code]]
In [14]: stdin, stdou, stderr = client.execute('uname -a')      

In [15]: stdou.readline()
Out[15]: 'Linux desktop-kb 2.6.29 #1 SMP Wed Apr 29 13:28:24 CEST 2009 i686 GNU/Linux\n'
[[/code]]
