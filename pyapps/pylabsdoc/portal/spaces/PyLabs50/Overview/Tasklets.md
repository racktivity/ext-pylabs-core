[ns]: /pylabsdoc/#/PyLabs50/NameSpaces
[dict]: http://docs.python.org/release/2.6.6/library/stdtypes.html#dict


## Tasklets

Tasklets are small pieces of code that are executed by a PyLabs Tasklet Engine. The tasklet engine is the component responsible for loading, categorizing, and executing tasklets. Tasklets are executed based on _tags_ and _priority_, but can also be triggered by events or other specific criteria.
Tasklets are used over the full PyLabs framework stack, from displaying wizards to storing object in a database.


### Tasklet Structure

In PyLabs, it is recommended that the file name of an action tasklet has the following structure:

`<priority>_<rootobject>_<action>.py`

* priority: integer value, indicating the priority of the tasklet, 1 is lowest priority 
* rootobject: name of the Root Object, all lower-case
* action: name of the action, as defined in the interface file of the proper Root Object

Tasklets have always the structure as shown below:

[[code]]
__author__ = 'incubaid'
    
def main(q, i, p, params, tags):
    code to implement action

    params['result']=something

def match(q, i, p, params, tags):
    return True
[[/code]]

The tags of the tasklet are the folder names in which the tasklet resides. Take a look at the action tasklet `1_customer_create.py` of the 'sampleapp'.
This file is located in `/opt/qbase5/pyapps/sampleapp/impl/action/crm/customer/create`, where `crm` is a domain inside the 'sampleapp' application. All folder names, including the domain name, are used as tags of the tasklet.
Thus the tags of the given tasklet example are `crm`, `customer`, and `create`.

In PyLabs 5 you can still use the old style tasklets, where the priority and tags are inside the tasklet. In that case the tags and priority override the folder and file name usage as described above.
An oldstyle tasklet then looks like:


[[code]]
__author__ = 'incubaid'
__tags__ = 'crm', 'customer', 'create'
__priority__ = 1
    
def main(q, i, p, params, tags):
    code to implement action

    params['result']=something

def match(q, i, p, params, tags):
    return True
[[/code]]


### The Tasklet Main-Function
The `main` function of a tasklet contains the code that will be executed when the tasklet is triggered. In this function you can use all PyLabs [name spaces][ns] (i, p, and q).
Besides the three name spaces you get a [dictionary][dict] of parameters and a tuple of tags.
If you need more libraries in your function, you can import them inside this function.

[[code]]
def main(q, i, p, params, tags):
    import time
    now = time.time()
    code to implement action

    params['result']='something'
[[/code]]    

The `tags` contain the tags used to call the tasklet. The tags tuple is not necessarily required to be exactly the same as the tags build via the folder names or inside the tasklet.

The `params` dictionary can contain a set of key-value pairs. This dictionary is populated throughout the whole PyLabs framework. 
As shown in the example above, you add the value `something` to the key `result`. If you call another tasklet with the same `params` dictionary, the dictionary has one more key-value pair, compared to the one used in the shown tasklet.

Beware that a tasklet should execute one and only one task, so don't execute more than one task in the tasklet.


### The Tasklet Match-Function
The `match` function is the first function that is executed when a tasklet is triggered. If the function returns `True`, then the `main` function of the tasklet is executed. 
When the `main` function must be executed without specific filters, which means that the tasklet is triggered by tags only, then you can omit the `match` function in the tasklet.
This could be done in the shown example.

If the `main` function may only be executed in certain cirumstances, you can add the criteria to the `match` function. 
Similar to the `main` function, you can use all PyLabs [name spaces][ns] (i, p, and q), you have a [dictionary][dict] of parameters and a tuple of tags at your disposal, and you can import extra libraries if required.

In the example below, the tasklet is only executed every 300 seconds or five minutes.

[[code]]
def match(q, i, p, params, tags):
    import time
    return (params['taskletlastexecutiontime']  + 300 <= time.time())
[[/code]]