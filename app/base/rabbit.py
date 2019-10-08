from datetime import datetime
import time
import traceback
import unittest
import pika
from flask import jsonify
from app.base.loggerNoSQL import loggerNoSQL, kindOfLog
from app.base.QBase import qBase

class taskMQ(unittest.TestCase):

    def __init__(self, idUser, host='localhost'):
        """
        to start the RabbitMQ server, open your terminal and type:
        
        export PATH=$PATH:/usr/local/opt/rabbitmq/sbin
        Rabbitmq-server <enter>

        to access management panel open your browser and type http://localhost:15672 by default
        """

        cnn = rabbitMQConnection(idUser, host)
        self.connection = cnn.connection
        self.channel = cnn.channel
        self.queueNames = cnn.queueNames
        del cnn

        self.__loggerNoSQL = loggerNoSQL()
        self.__idUser = idUser
        self.qBase = qBase()

    def sendMessage(self, queueName=str, bodyMessage=str):
        """
        Creates a Queue to send message to broker 
        Parameters:
            queueName: Label that specifies a Queue
            bodyMessage: message to send 
        """
        self.channel.queue_declare(queue=queueName, durable=True)

        self.channel.basic_publish(exchange='',
                      routing_key=queueName,
                      body=bodyMessage,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

        self.connection.close()

        return True

    def testSendMessage(self, queueName=str, bodyMessage=str):
        try:
            self.assertTrue(self.sendMessage(queueName, bodyMessage))

            return self.qBase.toJsonRoute("Message sent", 200)
        except AssertionError as ae:
            _message = ae.args[0]
            self.__loggerNoSQL.insertLog(_message, kindOfLog.ERROR, traceback.format_exc(), self.__idUser)

            return self.qBase.toJsonRoute("Error on send your message\n" + 
                "Please check the log information", 500)

class workerMQ(unittest.TestCase):

    def __init__(self, idUser, host='localhost'):
        """
        to start the RabbitMQ server, open your terminal and type:

        export PATH=$PATH:/usr/local/opt/rabbitmq/sbin

        Rabbitmq-server <enter>

        to access management panel open your browser and type http://localhost:15672 or 5672 by default
        """

        self.port = 15672

        cnn = rabbitMQConnection(idUser, host)
        self.connection = cnn.connection
        self.channel = cnn.channel
        self.queueNames = cnn.queueNames
        del cnn

        self.__loggerNoSQL = loggerNoSQL()
        self.__idUser = idUser
        self.qBase = qBase()

    def __enter__(self):
        self.testRunWorker()

    def add_dynamic_function(self, description):
        fn_name = 'callback_' + description

        def fnCallback(self, ch, method, properties, body):
            print(" [x] Received %r" % body)

        setattr(workerMQ, fn_name, fnCallback)

        return fnCallback

    def runWorker(self):

        self.channel.queue_declare(queue=taskQueueName.LOG_INFO(), durable=True)

        print('Rabbit MQ worker is running and waiting for messages. Press CTRL+C to exit')

        def callback(ch, method, properties, body):
            print("Received %r" % body)
            time.sleep(1)
            print("Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=taskQueueName.LOG_INFO(), on_message_callback=callback) 

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.connection.close()
            return True

        return False

    def __exit__(self, type, value, tb):
        pass

    def testRunWorker(self):
        try:
            self.assertTrue(self.runWorker())

            return jsonify({ "message": "" }), 200

        except AssertionError as ae:
            return jsonify({ "message": ae.args[0] }), 500

class rabbitMQConnection(unittest.TestCase):

    def __init__(self, idUser, host='localhost'):
        """
        to start the RabbitMQ server, open your terminal and type:

        export PATH=$PATH:/usr/local/opt/rabbitmq/sbin <enter>
        Rabbitmq-server <enter>

        to access management panel open your browser and type http://localhost:15672 or 5672 by default
        """

        self.connection = None
        self.channel = None
        self.__loggerNoSQL = loggerNoSQL()
        self.__idUser = idUser
        self.qBase = qBase()
        self.host = host
        self.port = 15672

        self.queueNames = [
            taskQueueName.EXCEPTION_ERROR(), 
            taskQueueName.LOG_INFO(), 
            taskQueueName.SEND_MAIL()
            ]

        self.testConnection()

    def startsConnection(self):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()

        return True

    def testConnection(self):
        try:
            self.assertTrue(self.startsConnection())
        except AssertionError as ae:
            _message = ae.args[0]
            self.__loggerNoSQL.insertLog(_message, kindOfLog.ERROR, traceback.format_exc(), self.__idUser)

            return self.qBase.toJsonRoute("Unable to connect on Rabbit MQ server\n" + 
                "Please check in your terminal if there is rabbitMQ server started on port {}".format(str(self.port)), 500)

    def __del__(self):
        pass

class taskQueueName:

    @staticmethod
    def EXCEPTION_ERROR():
        return 'EXCEPTION_ERROR'

    @staticmethod
    def LOG_INFO():
        return 'LOG_INFO'

    @staticmethod
    def SEND_MAIL():
        return 'SEND_MAIL'

with workerMQ(1) as mq:
    print('\nFinish in ' + datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M'))
