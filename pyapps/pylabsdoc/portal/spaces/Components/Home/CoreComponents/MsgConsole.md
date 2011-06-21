@metadata title=Message Console
@metadata tagstring=message console


# PyLabs Message Console

* lets call for now messageconsole (NO LONGER logserver)
* logs to stdout all kind of messages

## Principles

* output to stdout using print (do not use PyLabs primitives)
* reformat message message to fit nicely on screen (use screenwidth param)

    ** messages -> get nicely formatted
    ** /n as enter

* provide startup options q.console.start(screenwidth=120, ...)

    ** screenwidth (std 120)

## Interactivity

* implement possibility to control messageconsole (filters)


@todo check implementation
    #include which apps to see and not to see (defined as part of sourcestring)
    q.messages.console.filterSourceApplications(includes[],excludes=[])  #e.g. includes=["*test*"]
    #show list of all applications found so far in active messageserver session and allow selection of which ones to see or not to see (multiple)
    i.messages.console.filterSourceApplications(sinceXNrMinutes=0)
    
    # show dropdown (in console) to select min or max level, show explanation of what the level is
    i/q.messages.console.setMinLevel()
    i/q.messages.console.setmaxLevel()
    
    #allow multi selection of types to see e.g. errorcondition, ...  (use an enumerator)
    q.messages.console.filterOnType(includes=[],excludes=[])
    i.messages.console.filterOnType()
    
    #filter on tags
    q.messages.console.filterOnTags(includes=[],excludes=[]) #e.g. includes=["customer:kris* invoice","urgent"]
    i.messages.console.filterOnTags(sinceXNrMinutes=0)  #show possibilities since last X minutes
    
    #makes it easy for user to find which tags have been used, this is quite generic can be used to e.g. filter on agents, ...
    i.messages.console.showFoundTags(sinceXNrMinutes=0)


##How to communicate with console socket server?

* do this by implementing a control mechanism on the socket of the console socket server

e.g. (free to change but be pragmatic)

    ::cmd:: setMinLevel 7
