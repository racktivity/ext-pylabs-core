## Commands Over XMPP

### Agent

* agent register xmppserver

    !agent register
    xmppserver
    !

* agent register $xmppserver1 $xmppserver2, ...  \#can register to multiple xmppservers

    !agent register
    xmppserver1
    $xmppserver2
    ...
    $xmppservern
    !

* agent passwd $newpasswd #set a new passwd for the agent

    !agent register
    newpasswd
    !


### Authentication and Permissions (*)

* perm set $agentsfilter $acl #set permissions for agent
* this can only be done for user which has perm:1 rights

    !perm set
    *@superadmin.eur.daas.com
    $*@cloud1.ghent.goodguys.com
    $all:1
    !

* perm delete $agentsfilter

    !perm delete
    *@superadmin.eur.daas.com
    !
**Important** -- this instruction will not remove the permissions for \*@cloud1.ghent.goodguys.com

* perm list
* dump all permissions


### (q)shellcmd

* shellcmd \-$stringWhateverNeedsToBeExecuted    #theString can be multiple lines
    ** options
        *** `-no` means NoOutput, output (stderr and stdout) will not be sent back

    !shellcmd
    stringWhateverNeedsToBeExecuted
    !

* qshellcmd -$stringWhateverNeedsToBeExecutedInQshellScript
    ** options
        *** `-no` means NoOutput, output (stderr and stdout) will not be sent back
        *** `-l5` means send pylabslogging over xmpp till loglevel 5
        *** `-params` $validPythonDictionary (e.g: `-params {'param0': 'test', 'counter':1}`)

    !qshellcmd
    -params {'param0': 'test', 'counter':1}
    $ stringWhateverNeedsToBeExecuted
    !

* every shellcmd & qshellcmd is executed in separate process


### Q-Packages (v4)

* qpackages update
* qpackages setsource $sourcestring of config file for qpackages (allows to redirect to other qpackages server)
* qpackages emptycache  #removes all tgz and other local cached apps, everything will be downloaded again
* qpackages install $name:$version:$domain  #version & domain optional
* e.g. qpackages install kdstest::test.domain.com  #empty version here, so not relevant
* if more than 1 found, error

    !qpackages update
    !
    
    !qpackages setsource
    sourcestring
    !
    
    !qpackages emptycache
    !
    
    !qpackages install
    name
    $version
    $domain
    !

* These commands are implemented for qpackagesV3 only till now.


### Portforward

* portforward `-R $serverport:$localdestination:$portondestination $login:$passwd@$sshServerInPubDC`  
@todo check can we get it to work using passwds?

    !portforward
    -R
    $1234
    $machineOnInternalSSONet
    $22
    $root@sshserverInDAAS    #now ssh to sshserverindaas on port 1234 will arive on machineOnINternalSSONet
    !

* portforward `-L $serverport:$localdestination:$portondestination $login:$passwd@$sshServerInPubDC`  
@todo check can we get it to work using passwds?

* syntax used is very close to original SSH syntax


### Kill/Stop Tasks

* this command kills or stops task given its task number
* syntax

    !task kill
    <tasknr>
    !
    
    !task stop
    <tasknr>
    !

* example

    !task kill
    203
    !
    
    !task stop
    104
    !


### File Systems, File, ... (*)

* download $cloudfsUrl $localpath
* upload $localpath $cloudfsUrl
* file read $filepath
* file write $filepath $content
* fs listdrives #show found partitions, only relevant for windows e.g. c: e: ...
* fs dir $path  #return list of files/dirs/links in path
* fs stat $path
* fs delete $path


#### Format of Return of Dir

    $filename f $size
    $dirname d
    $linkname l


### qbase (*)

* qbase install $tgzlocationOfNewSandbox $destinationpath #if not dest put in /opt/qbase5 of unix and c:\qbase5 for windows
    **mark in registry when windows what qbase location is
* qbase getlocation  #show location of sandbox (only relevant for windows)


### dialog (*)

* dialog message $message #which will popup on screen where icon is running
* rdp $login:$passwd@$dest:$port


### taskbar (*)

* taskbar icon enable  #enable taskbar agent with logo of agent
* taskbar icon disable
* taskbar icontooltip $tooltipmessage #e.g. "downloading of qbase 90%"


### askpermission (*)

* askpermission $message  #tells agent to ask permission use optional message how to ask permission
    ** askpermission also asks for how long permission should be given, std 1h
    ** otherwise user would have to reconfirm all the time
    ** only relevant for cmd's which need permission to run


### system processes

* system setpasswd $username $passwd
* process list
* process kill
* process hardkill
* system reboot

    !system setpasswd
    username
    $passwd
    !
    
    !process list
    !


### future (*)

FUTURE
* system service start $servicename
* system service stop $servicename
* system service list
* dialog askpath  #future
* dialog question $question #ask a string question e.g. what is name of your mother
* dialog dropdown $question $dropdownAsCommaSeparated #show dropdown and ask to choosed

* cloudapi $category $method $params returnformat=$returnmethod
    ** returnformat= HR, YAML     #HR = human readable


### scheduler

* scheduler start  #starts scheduler as service/daemon which works with the tasklets see [AgentV4Scheduler]
* scheduler stop