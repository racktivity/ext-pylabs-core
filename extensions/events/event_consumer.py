from pylabs import q
from pylabs.InitBase import q
import rabbitmqclient as rmq
import events
from events import EXCHG_NAME, EXCHG_TYPE

class EventConsumer :

    def __init__ ( self, queueName, bindingKey, taskletDir ):
        self._connection = rmq.Connection()
        self._queueName = queueName
        self._exchangeName = EXCHG_NAME
        self._exchangeType = EXCHG_TYPE
        self._bindingKey = bindingKey
        self._taskletEngine = q.getTaskletEngine ( taskletDir )

    def consume( self ) :
        self._connection.declareExchange( self._exchangeName, self._exchangeType )
        self._connection.declareQueue( self._queueName )
        self._connection.declareBinding( self._exchangeName, self._queueName, self._bindingKey )

        def handle_one_event( event ) :
            params = dict() 
            params['eventKey'] = event.routing_key
            params['eventBody'] = event.body
            print params
            self._taskletEngine.execute( params )

        print self._queueName
        self._connection.consume( self._queueName, handle_one_event )
        
          
if __name__ == '__main__':
    import sys
    
    cmdArgs = sys.argv
    if len( cmdArgs ) != 4:
        print cmdArgs
        raise RuntimeError( "Usage: eventconsumer.py queuename bindingkey taskletdir" )
    cons = EventConsumer( cmdArgs[1], cmdArgs[2], cmdArgs[3] )
    cons.consume()

