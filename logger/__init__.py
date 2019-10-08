from flask_restful import Api
from mainLogger import flaksApp
from .taskLogger import taskLogger

restServer = Api(flaksApp)

restServer.add_resource(taskLogger, "/logger/v1.0/taskLogger")