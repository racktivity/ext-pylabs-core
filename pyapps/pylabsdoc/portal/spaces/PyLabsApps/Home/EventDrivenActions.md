@metadata title=Event-Driven Actions
@metadata order=90
@metadata tagstring=event actions event-driven

[rabbit]: http://www.rabbitmq.com/
[pyappdir]: #/PyLabsApps/Introduction
[events]: #/Overview/Events

#Event-Driven Actions
In the previous sections you have learned how to create actions. These actions are all triggered by manual intervention, for example creating an object.

In many cases you want actions to be executed automatically, for example send a mail to a new customer, or update a page when an object is updated.


##PyLabs 5 Events
Pylabs 5 introduces a new standardized way for publishing and consuming [events][] using tasklets. The event framework uses [RabbitMQ][rabbit] as messaging system. The three important components in this event framework are:

* Producer: publishes event messages in a specific format
* Consumer: reads the event messages in the RabbitMQ network and triggers an action if the event message matches specific criteria
* Message Queue: this is a sort of mailbox in which the producer publishes the event messages

Each application is able to define multiple consumers which are registered for certain types of events. These events can be published by any application and be consumed by any other application.


##Event Structure
An event in PyLabs 5 consists of two strings. The first string is the 'event' key, used to categorize the event. The second string can span multiple lines, where each line is a PyLabs tags/label-string. For example:

    customer_pending state:created guid:5a1b2969-7f7f-46b0-a0f8-4060f5f8ca5b
    status:new guid:1fdcd5cd-e9a5-4f3c-a329-f6ed72f790e2


##Event Producer
If your application, or an action in your application, must publish an event, you must execute the following API call:
    
    p.events.publish(routingKey, tagString)

The `routingKey` is a dot separated which has always the prefix `pylabs.event.<appname>`. For more specific categorization you can extend the prefix.

For example, you can create an event when a mail has arrived in a mailbox:

    p.events.publish('pylabs.event.sampleapp.email', 'mail:%s'%base64.encodestring(mail))

The routing key is '`pylabs.event.sampleapp.email`'. Each event consumer that has this key in its configuration file will react on this event.

PyLabss 5 has already some built-in producers, located in `/opt/qbase5/pyapps/sampleapp/impl/osis/generic/object_generateevent_<action>.py`. These producers generate events for objects stored/updated in or deleted from OSIS.

[[code]]
__author__ = 'incubaid'
__tags__ ='osis', 'store'
__priority__= 1

def main(q, i, p, params, tags):
    root = params['rootobject']
    domain = params['domain'] 
    p.events.publish('pylabs.event.sampleapp.osis.store.%s.%s' % (domain, root.PYMODEL_MODEL_INFO.name), root.guid)
[[/code]]
    

##Event Consumer
A PyLabs event consumer is a client that reacts on a given event. The consumer consists of a configuration file and at least one tasklet.

The configuration file has one section `[main]` with the following entries:

    [main]
    event_key = pylabs.event.crm.lead.#
    workers = 1


##Event Key
Two wildcards are allowed in the event_key entry:

* `*`: matches a single word delimited by periods
* `#`: matches none or more words, not delimited by periods

Take for example the following event_key: `pylabs.event.crm.*.cancel.#'`

The events with following routing keys will match:

    pylabs.event.crm.operation.cancel
    pylabs.event.crm.operation.cancel.by.user

The events with following routing keys will not match:

    pylabs.event.crm.user.operation.cancel
    pylabs.event.crm.cancel.operation.confirmed


##Workers
The number of workers define how many processes can be started. Each process will be a instance of a tasklet engine. The incoming events, matching the event key, are distributed over the worker processes in a load balanced way. 


##Example Consumer
You must create the consumer files in the following directory: `<pyapp name>/impl/events/<event process>`. See the [PyApps Directory Structure][pyappdir] for more information about the location of the files.

For example, when customer data changes, its page must be created or updated. Instead of manually launching the creation or update of the page, an event can be generated and a consumer can trigger the action to create of update the page.


###Creating the Configuration File
The configuration file defines when an action needs to be executed. The configuration file must have the name `consumer.cfg`.

    [main]
    eventKey = pylabs.event.sampleapp.osis.#
    workers = 1


###Creating the Action Tasklet
A consumer can have more than one action tasklets. Therefore it is very important to know which action tasklet must be executed upon an event creation. The `params` dictionary in this tasklet always receives two keys. 

* `eventKey`: the event key published in the evnet message
* `eventBody`: the multi-line tag/label-string, being the body of the event message

Each action tasklet must have a match function in which you define what the `eventKey` must be. The following example shows a tasklet that is executed when a customer is removed from OSIS.

[[code]]
def match(q, i, params, tags):
    return params["eventKey"]=='pylabs.event.sampleapp.osis.delete'
[[/code]]    

The main function contains the actions to be executed. The following example is a simple action that deletes a page with a specific GUID. The GUID is retrieved from the `eventBody` key of the `params` dictionary.

[[code]]
def main(q, i, p, params, tags):
    guid = params["eventBody"]
    p.action.ui.page.delete(guid)
[[/code]]


##Conclusion
The event framework is a simple, but powerful component of the PyLabs framework. Its major feature is the possibility of event-driven actions.
An event-driven action is an action that is executed when a specific event is generated. You have to decide yourself when to generate an event. Do not exaggerate however, it may slow down your application.
Typically a PyApp has multiple consumers, each reading the events (messages) published on the RabbitMQ queue. A consumer consists of a configuration file and one or more action tasklets. The configuration file filters the events by using the eventKey. The `match` function in the action tasklet then determines which tasklet needs to be executed.


