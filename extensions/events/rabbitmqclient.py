# -*- coding: utf-8 -*-
#INCUBAID BSD version 2.0
#Copyright © 2010 Incubaid BVBA
#
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or
#without modification, are permitted provided that the following
#conditions are met:
#
#* Redistributions of source code must retain the above copyright
#notice, this list of conditions and the following disclaimer.
#
#* Redistributions in binary form must reproduce the above copyright
#notice, this list of conditions and the following disclaimer in    the documentation and/or other materials provided with the   distribution.
#
#* Neither the name Incubaid nor the names of other contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY INCUBAID "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL INCUBAID BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from pylabs import q
from amqplib import client_0_8 as amqp
import socket

class Connection(object):


    DEFAULT_EXCHANGE_NAME = 'main'
    DEFAULT_LEVEL = 5


    def __init__(self,server="127.0.0.1", port=5672, user="guest", password="guest", virtualhost="/" ):
        self._connected = False
        self._connection = None
        self._connectioninfo = (server, port, user, password, virtualhost)
        self.connect(*self._connectioninfo)

    def connect(self, server, port, user, password, virtualhost) :
        try:
            self._connection = amqp.Connection(host='%s:%d'%(server, port), userid = user, password = password, virtual_host = virtualhost, insist = False)
        except Exception:
                raise RuntimeError('Could not connect to RabbitMQ server using host: %s, port: %d, userid: %s, password: %s, virtualhost: %s . Is the server up and running on this port?'%(server, port, user, password, virtualhost))
        self._channel = self._connection.channel()
        self._connected = True
        #@tdo: dont open the three channels that early probably you will have multiple instances of this class one for reading and other for writing
        self._channel = self._connection.channel()
        self._readerChannel = self._connection.channel()
        self._writerChannel = self._connection.channel()
        self._consumerChannel = self._connection.channel()
        self._host = server
        self._port = port
        self._userid = user
        self._password = password
        self._virtualhost = virtualhost


    def publish(self, exchangeName, routingKey, message, deliveryMode=2, messageProperties=None, closeConnection=False):
        """
        Publish the message to an exchange using a specific routingkey

        @param exchangeName: name of the exchange to publish the message to
        @param routingKey: the routingKey that will be used to forward the message to the appropriate queue
        @param message: message to put in the queue
        @param deliveryMode: the mode the message, by default the messages will persist on server reboot
        @param messageProperties: dictionary with AMQP message properties
        @param closeConnection:    close the connection after publishing the message
        """

        if not self.isConnected():
            q.console.echo('Your connection to RabbitMQ is not yet initialized, trying to connect to host: %s and port: %s'%(self._host, self._port))
            self.connect(*self._connectioninfo)
        #if there is a connection and no channel create one
        if not self._writerChannel.is_open:
            self._writerChannel = self._connection.channel()
        msg = amqp.Message(message)
        #making sure that the messages that didnt yet consumed  will be persisted upon reboot
        msg.properties['delivery_mode'] = deliveryMode

        # Update message properties
        if messageProperties:
            for k, v in messageProperties:
                msg.properties[k] = v

        try:
            self._writerChannel.basic_publish(msg, exchange = exchangeName, routing_key = routingKey)
            #needed to flush the message to the tcp socket

            if closeConnection:
                self._writerChannel.close()

        except amqp.AMQPChannelException, ex:
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            self.connect(*self._connectioninfo)
            if ex[0] == 404:
                raise ValueError('No Exchange found with name %s. Reason: %s'%(exchangeName, ex[1]))
            raise ex
        except socket.error, ex:
            self._connected = False
            q.logger.log('Failed to add item to the queue with routing key  %s. Make sure the server is up and running on host: %s and port: %s then call connect'%(routingKey, self._host, self._port), 5)
            raise RuntimeError('Failed to add item to the queue with routing key %s. Make sure the server is up and running on host: %s and port: %s then call connect'%(routingKey, self._host, self._port))


    def consume(self, queueName, callback, noAck=True):
        """
        Register a consumer for specific queue
        This method will not return until an exception occur to the channel

        @param queueName:     the name of the queue  the consumer will register to, one of the values of q.enumerators.QueueType.[Tab]
        @type queueName:      string

        @param callback:      python callable that will be invoked when new item is delivered to the queue
        @type callback:       python callable

        @param noAck:         If enabled, messages consumed do not need to be
                              acknowledged by the consumer to be flagged as
                              'processed' by the broker.
        @type noAck:          boolean
        """
        if not self.isConnected():
            q.console.echo('Your connection to RabbitMQ is not yet initialized, trying to connect to host: %s and port: %s'%(self._host, self._port))
            self.connect(*self._connectioninfo)
        try:
            self._consumerChannel.basic_consume(queueName, callback = callback, no_ack = noAck, consumer_tag = queueName)
            while True:
                self._consumerChannel.wait()
        except amqp.AMQPException, ex:
            self._connected = False
            raise RuntimeError('Failed to register a callback method %s .Reason: %s'%(callback, ex))
        finally:
            self._consumerChannel.basic_cancel(queueName)

    def consumeOneMessage(self, queueName):
        """
        Register a consumer for specific queue and consume 1 message.
        This method will not return until 1 message was consumed from the queue.

        @param queueName: the name of the queue  the consumer will register to, one of the values of q.enumerators.QueueType.[Tab]
        """

        global msg
        msg = None

        def receive(message):
            global msg
            msg = message

        callback = receive

        if not self.isConnected():
            q.console.echo('Your connection to RabbitMQ is not yet initialized, trying to connect to host: %s and port: %s'%(self._host, self._port))
            self.connect(*self._connectioninfo)
        try:
            self._consumerChannel.basic_consume(queueName, callback=callback, no_ack = True, consumer_tag = queueName)
            while True and not msg:
                self._consumerChannel.wait()
        except amqp.AMQPException, ex:
            self._connected = False
            raise RuntimeError('Failed to register a callback method %s .Reason: %s'%(callback, ex))
        finally:
            self._consumerChannel.basic_cancel(queueName)

        return msg




    def publishAndConsume(self, exchangeName, routingKey, message, returnExchangeName, returnRoutingKey, deliveryMode=2, message_properties=None, returnQueue=None):
        """
        Publish the message to an exchange using a specific routingkey and wait for a return message on the specified
        return exchange (and queue).
        This method is intended for synchronous RPC over queues.

        @param exchangeName: name of the exchange to publish the message to
        @param routingKey: the routingKey that will be used to forward the message to the appropriate queue
        @param message: message to put in the queue
        @param returnExchangeName: Exchange to which the return message will be sent
        @param returnRoutingKey: Routing key which will be used when publishing the return message
        @param deliveryMode: the mode the message, by default the messages will persist on server reboot
        @param message_properties: dictionary with AMQP message properties
        @param returnQueue: name of the queue to bind to the return exchange (=return routing queue if empty)
        """


        # Create temp infrastructure
        returnQueue = returnQueue or returnRoutingKey

        self.declareQueue(returnQueue, exclusive=True, durable=False, auto_delete=True)
        self.declareBinding(returnExchangeName, returnQueue, returnRoutingKey)

        # Publish message
        self.publish(exchangeName, routingKey, message, deliveryMode, message_properties)

        # Get response msg
        msg = self.consumeOneMessage(returnQueue)

        return msg



    def get(self, queueName):
        """
        Gets a message from a certain queue in rabbitMQ server

        @param queueName: name fo the queue to retreive an item from
        """

        if not self.isConnected():
            q.console.echo('Your connection to RabbitMQ is not yet initialized, trying to connect to host: %s and port: %s'%(self._host, self._port))
            self.connect(*self._connectioninfo)
        try:
            msg = self._readerChannel.basic_get(queueName)
            if msg:
                self._readerChannel.basic_ack(msg.delivery_tag)
                return msg.body
        except amqp.AMQPException, ex:
            #if there is an exception we need to reinitialize the client
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            self.connect(*self._connectioninfo)
            if ex[0] == 404:
                raise ValueError('No queue found with name %s. Reason: %s'%(queueName, ex[1]))
            raise ex
        except socket.error, ex:
            self._connected = False
            if ex[0] == 32:
                q.logger.log('Failed to get and item from the queue with name %s. Make sure the server is up and running on host: %s and port: %s'%(queueName, self._host, self._port), 5)
                raise RuntimeError('Failed to get item from the queue of name %s. Make sure the server is up and running on host: %s and port: %s then call initialize'%(queueName, self._host, self._port))
            raise ex
        return msg

    def disconnect(self):
        """
        Disconnect from the rabbitmq server
        """
        if self.isConnected():
            self._connected = False
            self._channel.is_open and self._channel.close()
            self._writerChannel.is_open and self._writerChannel.close()
            self._readerChannel.is_open and self._readerChannel.close()
            self._consumerChannel.is_open and self._consumerChannel.close()
            self._connection.close()


    def isConnected(self):
        return self._connected


    def declareExchange(self, exchangeName, exchangeType = 'direct', durable = True, auto_delete = False):
        """
        Declare a new exchange with a given name if not exist, if the exchange exists but with different configuration an exception will be raised

        @param exchnageName: name of the exchange to create
        @param exchangeType: can be one of three values fanout, direct, or topic
        @param durable: if true the exchange definition will be persisted upon server reboot
        @param auto_delete: if true the exchange will be deleted if no queues are binded to it
        """
        try:
            self._channel.exchange_declare(exchange= exchangeName, type= exchangeType, durable = durable, auto_delete = auto_delete)
        except amqp.AMQPConnectionException, ex:
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            self.connect(*self._connectioninfo)
            if ex[0] == 530:
                q.logger.log('The exchange %s is already exist but with different configuration. Maybe you should declare the exchange with different name'%exchangeName, 5)
                raise ValueError('The exchange %s is already exist but with different configuration'%exchangeName)
            raise ValueError('Failed to declare Exchange with name %s . Reason: %s'%(exchangeName, ex))
        except amqp.AMQPChannelException, ex:
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            raise RuntimeError('Failed to connect to the server using configuration host: %s, port: %s, userid: %s, password: %s, virtualhost: %s. Try to reinitialize your connection using connect mehtod'%(self._host, self._port, self._userid, self._password, self._virtualhost))


    def declareQueue(self, queueName, exclusive = False, durable = True, auto_delete = False):
        """
        Declare a new queue with given name if not exist, if the queue exists but with different configuration an exception will be raised

        @param queueName: name of the queue to declare
        @param exclusive: declare a private queue only the creator client can use it
        @param durable: if true the queue definition will be persisted upon server reboot
        @param auto_delete: if true the queue will be deleted if no consumers using it anymore
        """
        #str of the queue name in case of using the enums
        try:
            return self._channel.queue_declare(queue = str(queueName), exclusive = exclusive, durable = durable, auto_delete = auto_delete)
        except amqp.AMQPConnectionException, ex:
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            self.connect(*self._connectioninfo)
            if ex[0] == 530:
                q.logger.log('The queue %s is already exist but with different configuration. Maybe you should declare the queue with different name'%queueName, 5)
                raise ValueError('The queue %s is already exist but with different configuration'%queueName)
            raise ValueError('Failed to declare Queue with name %s . Reason: %s'%(queueName, ex))

        except amqp.AMQPChannelException, ex:
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            self.connect(*self._connectioninfo)
            raise RuntimeError('Failed to connect to the server using configuration host: %s, port: %s, userid: %s, password: %s, virtualhost: %s. Try to reinitialize your connection using connect mehtod'%(self._host, self._port, self._userid, self._password, self._virtualhost))


    def declareBinding(self, exchangeName, queueName, routingKey = None):
        """
        Declare a new binding, if the binding already exists the new one is agnored and no error is raised

        @param exchangeName: name of the exchange to bind the queue to
        @param queueName: the queue which will be binded to the exchanging
        @param routingKey: the routing rule that says deliver the message from the exchange to the queue if the message with this routing key, if not provided, will be the same as queueName
        """
        if not routingKey:
            routingKey = str(queueName)
        #str of the queue name in case of using the enums
        try:
            self._channel.queue_bind(queue = str(queueName), exchange = exchangeName, routing_key = routingKey)
        except amqp.AMQPException, ex:
            self._connected = False
            q.console.echo('Exception occured and the client needs to be reinitialized, reinitializing the client with the default values...')
            self.connect(*self._connectioninfo)
            raise RuntimeError('Failed to declare binding between exchange: %s and queue: %s using routingKey: %s. Reason: %s'%(exchangeName, queueName, routingKey, ex))



