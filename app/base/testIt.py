from datetime import datetime
import requests
import sys
import time
import traceback
import unittest
import pika
from pymongo import MongoClient, errors

class mongoRecipe(unittest.TestCase):

    def __init__(self):
        self.client = MongoClient("mongodb+srv://admin:100grillo@cluster0-sh419.mongodb.net/test?retryWrites=true&w=majority")
        self.idsInserted = []

        self.__testConnection()

    def checkServer(self):
        try:
            self.client.server_info()
            self.db = self.client.logRecipe

            return True
        except:
            return False

    def __testConnection(self):
        try:
            self.assertTrue(self.checkServer(), True)
        except AssertionError as ae:
            raise Exception('Failure to connect in database. \n',
                ae.args[0])

    def insertRecipe(self, date1, message):

        tb_logInfo = self.db.tb_logInfo

        result = tb_logInfo.insert_one({
            'ID_USER': 1,
            'DATE_OF': date1,
            'MESSAGE': message,
            'LEVEL': 'INFO',
            'TRACE': ''
        })

        return result._WriteResult__acknowledged

    def insertManyRecipes(self):
        lista = []

        [lista.append({
            'ID_USER': 1,
            'DATE_OF': '2019/09/15 18:55',
            'MESSAGE': f'Cake of ingredient{i}',
            'LEVEL': 'INFO',
            'TRACE': ''
        }) for i in range(1, 15)]

        db = self.client.logRecipe

        tb_logInfo = db.tb_logInfo

        results = tb_logInfo.insert_many(lista)

        [self.idsInserted.append(item) for item in results.inserted_ids]

        return True

    def findRecipe(self, title):
        tb_logInfo = self.db.tb_logInfo

        recipes = tb_logInfo.find({
            'MESSAGE': { '$gt': title }
        }).sort('MESSAGE', -1).limit(2).skip(0)

        lista = []
        for item in recipes:
            lista.append(item)

        return len(lista)

    def updateRecipe(self, title):
        tb_logInfo = self.db.tb_logInfo

        try:
            result = tb_logInfo.update({
                'MESSAGE': 'new Recipe 2'
            }, {
                '$set': {
                    'MESSAGE': title
                }
            }, multi=True)

            print(result['nModified'])
            return result['nModified']
        except:
            return 0

    def deleteRecipe(self, id):
        tb_logInfo = self.db.tb_logInfo

        result = tb_logInfo.delete_one({
            'MESSAGE': 'test'
        })

        return result

    def aggregate(self):
        self.db.tb_logInfo.aggregate({
            'MESSAGE':  '$Cheese'
        })

    def createIndex(self):
        self.db.tb_logInfo.create_index(
            [('DATE_OF', 1)],
            unique=True
        )

    def createTable(self, tableName=str, firstRec=dict):
        """
        Check if tableName is created, if don't it's create the table with fields
        described in firstrec variable
        """

        if tableName not in self.db.collection_names():
            tbl = self.db[tableName]

            tbl.insert_one(firstRec)
            tbl.delete_one(firstRec)

            return True

        return False

class taskMQ(unittest.TestCase):
    
    def __init__(self, idUser, host='localhost'):
        """
        to start the RabbitMQ server, open your terminal and type:

        Rabbitmq-server <enter>

        to access management panel open your browser and type http://localhost:15672 or 5672 by default
        """

        cnn = rabbitMQConnection(idUser, host)
        self.connection = cnn.connection
        self.channel = cnn.channel
        self.queueNames = cnn.queueNames
        del cnn

        self.__idUser = idUser

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

            return "Message sent"
        except AssertionError as ae:
            _message = ae.args[0]

            return "Erro"


class workerMQ(unittest.TestCase):
    
    def __init__(self, idUser, host='localhost'):
        """
        to start the RabbitMQ server, open your terminal and type:

        Rabbitmq-server <enter>

        to access management panel open your browser and type http://localhost:15672 by default
        """

        cnn = rabbitMQConnection(idUser, host)
        self.connection = cnn.connection
        self.channel = cnn.channel
        self.queueNames = cnn.queueNames
        del cnn

        self.__idUser = idUser

    def __add_dynamic_function(self, description):
        fn_name = 'callback_' + description

        def fnCallback(self, ch, method, properties, body):
            print(" [x] Received %r" % body)

        setattr(workerMQ, fn_name, fnCallback)

        fnCallback.__name__ = fn_name

        return fnCallback

    def __enter__(self):
        self.testRunWorker()

    def __exit__(self, type, value, tb):
        pass

    def runWorker(self):

        self.channel.queue_declare(queue=taskQueueName.LOG_INFO(), durable=True)

        print('Rabbit MQ worker is running and waiting for messages. Press CTRL+C to exit')

        def callback(ch, method, properties, body):
            print("Received %r" % body)
            time.sleep(body.count(b'.'))
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

    def testRunWorker(self):
        try:
            self.assertTrue(self.runWorker())
            return "OK"

        except AssertionError as ae:
            raise Exception(ae.args[0])

    def __del__(self):
        pass

class rabbitMQConnection(unittest.TestCase):

    def __init__(self, idUser, host='localhost'):
        """
        to start the RabbitMQ server, open your terminal and type:

        Rabbitmq-server <enter>

        to access management panel open your browser and type http://localhost:15672 or 5672 port by default
        """

        self.connection = None
        self.channel = None
        self.__idUser = idUser
        self.host = host

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

            return "Error"

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

# option = input('1 - Worker, 2 - Task:')

# if int(option) == 1:
#     with workerMQ(1) as mq:
#         print('\nFinish in ' + datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M'))

# elif int(option) == 2:
#     tMq = taskMQ(1)
#     tMq.testSendMessage(taskQueueName.LOG_INFO(), "An message for sample app")

# import signal
# import resource
# import os

# # To Limit CPU time
# def time_exceeded(signo, frame):
# 	print("CPU exceeded...")
# 	raise SystemExit(1)

# def set_max_runtime(seconds):
# 	# Install the signal handler and set a resource limit
# 	soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
# 	resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
# 	signal.signal(signal.SIGXCPU, time_exceeded)

# # To limit memory usage
# def set_max_memory(size):
# 	soft, hard = resource.getrlimit(resource.RLIMIT_AS)
# 	resource.setrlimit(resource.RLIMIT_AS, (size, hard))

# set_max_runtime(5)


# try:
#     assert mr.createTable('tb_user', rec) == True
# except AssertionError as ae:
#     trace = traceback.format_exc()

#     print(trace)

#     mr.insertRecipe(datetime.now(), trace)

# try:
#     assert mr.insertManyRecipes() == True
# except AssertionError as ae:
#     raise Exception('Error to insert many records \n' + ae.args[0])

# try:
#     assert mr.insertRecipe('2019/09/17 14:58', 'new Recipe 4') == True
# except AssertionError as ae:
#     raise Exception('Error to insert many records \n' + ae.args[0])

# try:
#     assert mr.findRecipe('new') > 0

# except AssertionError as ae:
#     raise Exception('No records found with this title condition \n' + ae.args[0])

# try:
#     assert mr.updateRecipe('Cheese Burger') > 0

# except AssertionError as ae:
#     raise Exception('No records found with this title condition \n' + ae.args[0])
