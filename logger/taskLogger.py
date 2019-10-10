from flask_restful import Resource
from flask import request
import requests
from app.views.responses import Responses
from app.base.loggerNoSQL import loggerNoSQL
from venv.config import Config

class taskLogger(Resource):

    def __init__(self):
        self.response = Responses()
        self.__loggerNoSQL = loggerNoSQL()

    def get(self):

        data = request.get_json(force=True)
        date = data['date']
        start = data['start']
        limit = data['limit']

        try:
            list1 = self.__loggerNoSQL.testListLogs(date, start, limit)
            
            return self.response.getResponse(200, str(list1))

        except Exception as err:
            return self.response.getResponse(500, err.args[0])

    def post(self):
        """
        Post request data for create a recipe
        Params:  message, kind, excep, user
        """

        data = request.get_json(force=True)
        message = data['message']
        kind = data['kind']
        excep = data['traceback']
        user = data['user']

        try:
            self.__loggerNoSQL.insertLog(message, kind, excep, user)

            return self.response.getResponse(200, "Success on logging")
        except Exception as err:
            return self.response.getResponse(500, err.args[0])

    def put(self):
        return self.response.getResponse(400, "Not implemented exception")

    def delete(self):
        return self.response.getResponse(400, "Not implemented exception")