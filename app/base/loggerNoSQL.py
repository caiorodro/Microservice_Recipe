from datetime import datetime
from enum import Enum
import requests
import unittest

from pymongo import MongoClient, errors
import traceback

from app.base.logger import logger
from app.base.QBase import qBase


class kindOfLog:

    @staticmethod
    def ERROR():
        return 'ERROR'

    @staticmethod
    def INFO():
        return 'INFO'

class loggerNoSQL(unittest.TestCase):

    def __init__(self):
        """
        Class that write and read logging on any kind info or error of the application
        """
        self.client = MongoClient("mongodb+srv://admin:100grillo@cluster0-sh419.mongodb.net/test?retryWrites=true&w=majority")
        self.idsInserted = []

        self.__testConnection()

        self.__listOfLogs = []

        self.__logger = logger()
        self.qBase = qBase()

    def checkServer(self):
        """
        Try to connect on MongoDB cloud instance and try to create collections

        Return: True if the database is reachable and False on any problem encontered on that
        """
        try:
            self.client.server_info()
            self.db = self.client.logRecipe
            self.__startTables()

            return True
        except:
            return False

    def __testConnection(self):
        """
        Tests the checkserver method to connect on database
        """

        try:
            self.assertTrue(self.checkServer(), True)
        except AssertionError as ae:
            raise Exception('Failure to connect in database. \n',
                ae.args[0])

    def insertLog(self, message, kind, trace, idUser):
        """
        Create a new log info or error and insert on database
        """

        tb_logInfo = self.db.tb_logInfo

        result = tb_logInfo.insert_one({
            'ID_USER': idUser,
            'DATE_OF': datetime.now().strftime('%m/%d/%Y %H:%M'),
            'MESSAGE': message,
            'LEVEL': kind,
            'TRACE': trace
        })

        self.__logger.logInfo(message)

        return result._WriteResult__acknowledged

    def listLogs(self, data, start, limit):
        """
        Creates a filtered list of collextion logs

        Return: returns a length of records found
        """
        tb_logInfo = self.db.tb_logInfo

        recipes = tb_logInfo.find({
            'DATE_OF': { '$gt': data }
        }).sort('DATE_OF', 1).skip(start).limit(limit)

        for item in recipes:
            self.__listOfLogs.append((item['DATE_OF'], item['LEVEL'], item['MESSAGE'], item['TRACE']))

        return len(self.__listOfLogs)

    def testListLogs(self, data, start, limit):
        """
        Tests the list of logs

        Return: returns the listOfLogs filled list 
        """

        try:
            self.assertGreater(self.listLogs(data, start, limit), 0)
        except AssertionError:
            pass

        return self.qBase.toJson(self.__listOfLogs)

    def newLog(self, message, kind, trace, idUser):
        """
        Creates a new using logging microservice on 127.0.0.1:5014
        by requesting this API through GET sending
        """

        result = None

        def testNewLog():
            URL = 'http://127.0.0.1:5014/logger/v1.0/taskLogger'

            PARAMS = { "message": message, "kind": kind, "traceback": trace, "user": idUser }

            result = requests.post(url=URL, json=PARAMS)

            return result.status_code

        try:
            self.assertTrue(testNewLog(), 200)

            return { "message": message, "result": result }, 200

        except AssertionError as ae:
            return { "message": message, "result": 'Error on create log ' + ae.args[0] }, 500
        
    def __startTables(self):
        """
        Starts to create table collections if they don't created yet
        """

        tables = [{"tableName": "tb_logInfo",
                   "firstRec": {
                       "ID_USER": 1,
                        "DATE_OF": datetime.now().strftime('%m/%d/%Y %H:%M'),
                        "MESSAGE": "",
                        "LEVEL": 'INFO',
                        "TRACE": ""
                    }
                }, {"tableName": "tb_user",
                   "firstRec": {
                        "ID_USER": 1,
                        "EMAIL": "caiorodro@gmail.com",
                        "NAME": "Caio Rodrigues"
                    }
                }]

        for item in tables:
            self.__createTable(item['tableName'], item['firstRec'])

    def __createTable(self, tableName, firstRec):
        """
        Check if tableName is created, if don't it's create the table with fields
        described in firstRec variable

        Return: 
            returns True if table was successfully created
        """
        if tableName not in self.db.collection_names():
            tbl = self.db[tableName]
            tbl.insert_one(firstRec)
            tbl.delete_one(firstRec)

            return True

        return False