from flask_restful import Resource
from flask import request
import logging as logger
from app.views.user import user
from app.base.mapTable import mapUser
from app.views.responses import Responses

from venv.config import Config

class taskUser(Resource):

    def __init__(self):
       self.response = Responses()

    def get(self):

        logger.debug("Try to get users list")

        data = request.get_json(force=True)
        keep = data['keep']
        name = data['name'] if len(data['name']) > 0 else None
        email = data['email'] if len(data['email']) > 0 else None

        result = user(keep).listUsers(name, email)

        return self.response.getResponse(200, result)

    def post(self):
        logger.debug("Inside post me")

        data = request.get_json(force=True)
        keep = data['keep']

        u = mapUser(
            int(data['ID_USER']),
            data['NAME'],
            data['PASSWORD'],
            data['EMAIL'],
            int(data['KIND)F_USER']),
            int(data['USER_ENABLED'])
        )

        try:
            user(keep).saveUser(u)
        except Exception as err:
            return self.response.getResponse(500, err.args[0])

        return self.response.getResponse(200, "User saved")

    def put(self):
        logger.debug("Inside put me")
        return self.response.getResponse(200, "inside put method by Id: {}".format('0'))

    def delete(self):
        logger.debug("Inside delete me")

        data = request.get_json(force=True)
        keep = data['keep']

        try:
            user(keep).deleteUser(data['ID_USER'])
            return self.response.getResponse(200, "Successfull on delete action")
        except Exception as e:
            return self.response.getResponse(500, e.args[0])
