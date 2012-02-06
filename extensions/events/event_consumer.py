from pylabs.InitBase import q, p
import rabbitmqclient as rmq
from events import EXCHG_NAME, EXCHG_TYPE, MULTICONSUME_NAME
from functools import wraps
import traceback

def safe(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            t = traceback.format_exc()
            q.logger.log("Caught exception while executing %s: %s" % (func, t), 2)
    return wrapped_func

class EventConsumer:
    """
    Connects to a Rabbitmq server as a consumer
    """

    def __init__ ( self, queueName, bindingKey, taskletDir, host):
        q.logger.log("Creating event consumer on queue %s with binding key %s and tasklet dir %s" % (queueName, bindingKey, taskletDir), 7)
        self._connection = rmq.Connection(host)
        self._queueName = queueName
        self._exchangeName = EXCHG_NAME
        self._exchangeType = EXCHG_TYPE
        self._bindingKey = bindingKey
        self._taskletEngine = q.taskletengine.get(taskletDir)
        q.logger.log("Event consumer %s started" % self, 7)

    def consume( self ) :
        self._connection.declareExchange( self._exchangeName, self._exchangeType )
        if self._queueName != MULTICONSUME_NAME:
            self._connection.declareQueue( self._queueName )
        else:
            #we want multiple consumers to each parse the events so we let the server create a unique queue name
            self._queueName, _, _ = self._connection.declareQueue("", exclusive=True)
        self._connection.declareBinding( self._exchangeName, self._queueName, self._bindingKey )

        @safe
        def handle_one_event( event ) :
            q.logger.log("Event consumer %s: handling event %s" % (self, event), 7)
            params = dict()
            params['eventKey'] = event.routing_key
            params['eventBody'] = event.body
            self._taskletEngine.execute( params )

        self._connection.consume( self._queueName, handle_one_event )

    def __str__(self):
        return "Event Consumer <%s>" % self._queueName


if __name__ == '__main__':
    import sys
    cmdArgs = sys.argv
    if len(cmdArgs) != 5:
        print cmdArgs
        raise RuntimeError( "Usage: eventconsumer.py queuename bindingkey taskletdir" )
    queueName, bindingKey, taskletDir, appName = cmdArgs[1:]
    dirname = q.system.fs.getBaseName(taskletDir)
    q.application.appname = "../%s/eventconsumer/%s" % (appName, dirname)
    q.application.start()
    p.api = p.application.getAPI(appName)
    p.api.model = p.application.getAPI(appName, context=q.enumerators.AppContext.APPSERVER).model
    host = p.application.getRabbitMqHost(appName)
    cons = EventConsumer(queueName, bindingKey, taskletDir, host)
    cons.consume()
