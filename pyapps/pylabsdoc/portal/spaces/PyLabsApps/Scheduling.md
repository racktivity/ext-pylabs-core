[reality]: /pylabsdoc/#/PyLabsApp/Reality
[pyappdir]: /pylabsdoc/#/PyLabsApp/SampleApp


#Scheduling Actions
In many cases it is desirable that certain actions are executed on a regular basis. In such a situation you can create scheduled actions.
A scheduled action can launch event-driven actions; for example check a mailbox every five minutes, where an event can be thrown when mails have arrived.

For more details about the setup of the mail server in this sample application, see the [From DRP to Reality section][reality].


##Creating a Scheduled Action
Similar to all other actions of a PyApp, scheduled actions too are tasklets. These tasklets must have the following characteristics:

* a specific `match` function, which defines the execution interval of the action
* at least the tag `schedule`

The structure of the scheduled tasklet should look like this:

[[code]]
__tags__ = 'schedule'
__author__ = 'incubaid'
    
def main(q, i, p, params, tags):
    pass
        
def match(q, i, p, params, tags):
    your schedule code here        
[[/code]]
 
The tasklet is located in `<pyapp name>/impl/schedule/`. To keep a clear overview on the different scheduled actions, you can create a subdirectory per action, for example:

    <pyapp name>/impl/schedule/config/<config app>/
    
See the [PyApps Directory Structure][pyappdir] for more information about the location of the files.


##PyLabs Scheduling
To make scheduling possible in PyLabs, there is a specific application server service that runs every 60 seconds. This 'scheduling' service requests the tasklet engine to see if there are tasklets to be executed.
The tasklet engine keeps track of the last execution time of each tasklet. This execution time can be used in the `match` functions to  define the interval between two executions.


##Defining the Interval
In the `match` function you must import the standard Python `time` library. The `params` dictionary, which is used throughout the complete PyLabs framework, keeps track of the execution time of a tasklet with the key `taskletexecutiontime`. This allows us to set the interval for the tasklet.

[[code]]
def match(q, i, params, tags):
    import time
    return (params['taskletlastexecutiontime']  + 300 <= time.time())
[[/code]]        
       

The example above shows us that the tasklet is executed when the interval is more than 300 seconds.


##Conclusion
A scheduled action is a conventional action which is executed on a defined schedule, resulting in less human interaction.
