@metadata title=Process Handler
@metadata tagstring=process handle tasklet engine

# PyLabs Process Handler

* run a process per processhandlerdirectory
* per process run a taskletengine which runs a main loop with params which are always given to each tasklet, the params stay in memory 
* the parameters used when starting the taskletengine are coming from or

    ** a YAML file = `$qbasedir/cfg/processhandler/$processgroupname/params.yaml`
    ** an inifile = `$qbasedir/cfg/processhandler/$processgroupname/params.ini`  \#only supports params & arrays of params, values are int or string   

    [main]
    $paramname=$paramvalue
    $paramname=$paramvalue1,$paramvalue2

## Process Handler

* main loop which calls tasklet engine every 10 second to execute on all tasklets  
* in tasklets the match function implements its own scheduling (e.g. after 23h, once a day)
* when match the main function executes what needs to be done
* priorities of tasklets need to be used when executing the tasklets in the loop
* when params\["break"\]=True set by one of tasklets, than the other tasklets part of loop are not executed, 10 sec later the process starts over again
* a separate process per schedulegroup


## usecases

* monitoring capturing tasklets
* monitoring rules
* autostart of services

    ** use sal's of other dependant services to check status only if the other services are running then start our own service
    ** check if own service is running if not start
    ** e.g. juggernautdb requires zookeeper, juggernaut checks is there zookper running, if yes I run too


## directory structure processhandler

each dir implements a `$processgroup`
`$qbasedir/apps/processhandler/$processgroupname/`

    [qbase]/apps/processhandler/monitoringcapture/
    [qbase]/apps/processhandler/monitoringrules/$appname_$testdescription.py
    [qbase]/apps/processhandler/autostart/$appname.py
    [qbase]/apps/processhandler/autotasks/$appname.py  #generic task processhandler of whatever needs to be scheduled


## new install of application (FUTURE)

* when actor application.init() called 

    ** makes sure appropriate qpackages are installed
    ** when installing qpackage the appropriate tasklets get copied in processhandler
    ** the e.g. monitoring capture rules can be part of main qpackage or of sub qpackage or even a non related specific monitoring qpackage


## q... methods

    q.kernel.processhandler.stop($optionalschedulegroupname)  (informs agent that scheduling does not need to happen for now, then all looping over tasklets is stopped)
    q.kernel.processhandler.start($optionalschedulegroupname)
    q.kernel.processhandler.getstatus($optionalschedulegroupname)
    q.kernel.processhandler.getuptime()
    q.kernel.processhandler.getparams($processgroupname) #return params for that schedulegroup which are active right now
    ...
