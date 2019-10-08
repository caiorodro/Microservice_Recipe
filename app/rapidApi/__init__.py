from flask_restful import Api
from mainRapidAPI import app
from app.rapidApi.taskRecipe import taskManageRecipe

restServer = Api(app)

restServer.add_resource(taskManageRecipe, "/api/v1.0/taskManageRecipe")