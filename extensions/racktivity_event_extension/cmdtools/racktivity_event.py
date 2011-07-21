from pylabs import q, i
import simplejson

DEFAULT_QUEUE = 'racktivity.event.worker'
EXCHANGE_NAME = 'racktivity.event'
ROUTING_KEY = 'racktivity.event.#'

KEY_EVENTLEVEL = "eventlevel"
KEY_MESSAGE = "message"
KEY_MESSAGE_PRIVATE = "messageprivate"
KEY_TYPEID = "typeid"
KEY_TAGS = "tags"
KEY_ESCALATE = "escalate"

class RacktivityEventHandler(object):
    
    def __init__(self):
        """
        Initialization of the rabbitmq queue.
        """
        self.__connection = None
        try:
            self.__initcon()
        except Exception, e:
            q.logger.log("Failed to connect to rabbit MQ")
        
    def __initcon(self, force=False):
        if not self.__connection or force:
            self.__connection = q.queue.getRabbitMQConnection('racktivity_main')
            self.__connection.declareExchange(EXCHANGE_NAME)
    
    def reconnect(self):
        self.__initcon(True)
        
    def __publish(self, eventlevel, message, messageprivate="", typeid="", tags="", escalate=False):
        self.__initcon()
        message = {KEY_EVENTLEVEL: str(eventlevel),
                 KEY_MESSAGE: message,
                 KEY_MESSAGE_PRIVATE: messageprivate,
                 KEY_TYPEID: typeid,
                 KEY_TAGS: tags,
                 KEY_ESCALATE: escalate}
        
        messagedump = simplejson.dumps(message)
        
        self.__connection.publish(EXCHANGE_NAME, ROUTING_KEY, messagedump)
    
    def raiseCritical(self, message, messageprivate="", typeid="", tags="", escalate=False):
        """
        Raise a critical error
        """
        self.__publish(q.enumerators.ErrorconditionLevel.CRITICAL, message, messageprivate, typeid, tags, escalate)
        raise Exception(message)
    
    def raiseUrgent(self, message, messageprivate="", typeid="", tags="", escalate=False):
        """
        Raise a urgent error
        """
        self.__publish(q.enumerators.ErrorconditionLevel.URGENT, message, messageprivate, typeid, tags, escalate)
        raise Exception(message)

    def raiseError(self, message, messageprivate="", typeid="", tags="", escalate=False):
        """
        Raise a error
        """
        self.__publish(q.enumerators.ErrorconditionLevel.ERROR, message, messageprivate, typeid, tags, escalate)
        raise Exception(message)
    
    def raiseInfo(self, message, messageprivate="", typeid="", tags="", escalate=False):
        """
        Raise info
        """
        self.__publish(q.enumerators.ErrorconditionLevel.INFO, message, messageprivate, typeid, tags, escalate)
        
    def raiseWarning(self, message, messageprivate="", typeid="", tags="", escalate=False):
        """
        Raise a warning.
        """
        self.__publish(q.enumerators.ErrorconditionLevel.WARNING, message, messageprivate, typeid, tags, escalate)
        