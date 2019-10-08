from flask_restful import Api
from mainAuth import app
from app.views.taskUser import taskUser

restServer = Api(app)

restServer.add_resource(taskUser, "/api/v1.0/taskUser")