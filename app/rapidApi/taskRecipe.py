from flask_restful import Resource
from flask import request
import logging as logger
from app.base.authentication import authentication
from app.views.responses import Responses
from venv.config import Config
import requests

rapidAPIKey = "63facb4255mshb733c998f7d7f9bp128ac2jsn1587e6415a8b"
rapidAPIHost = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"

class taskManageRecipe(Resource):

    def __init__(self):
       self.response = Responses()

    def get(self):

        logger.debug("Try to get users list")

        data = request.get_json(force=True)
        keep = data['keep']
        result = ""

        return self.response.getResponse(200, result)

    def post(self):
        """
        Post request data for create a recipe
        """

        data = request.get_json(force=True)
        keep = data['keep']

        try:
            b1 = bytes(keep, encoding='utf-8')
            authentication.decode_auth_token(b1)
        except Exception as err:
            return self.response.getResponse(500, err.args[0])

        logger.debug("Log for create a new Recipe")

        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/visualizeRecipe"

        recipeData = {
            'backgroundImage': '', 
            'image': b'x',
            'ingredients': 'mozarela cheese, tomato, roust beefe or Ham, bread and butter',
            'instructions': 'On the on frying pan, cook the roust beef downside cheese in butter and low fire. Place two slices of tomatoes after chesse is melting, Finish with some grains of oregano.',
            'mask': 'starMask',
            'readyInMinutes': 5,
            'servings': 1,
            'title': 'Bauru sandwich'
             }

        payload = Responses.dictToStr(recipeData)

        headers = {
            'x-rapidapi-host': rapidAPIHost,
            'x-rapidapi-key': rapidAPIKey,
            'content-type': "multipart/form-data; boundary=---011000010111000001101001"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        return self.response.getResponse(200, response.text)

    def put(self):
        logger.debug("Inside put me")
        return self.response.getResponse(200, "inside put method by Id: {}".format('0'))

    def delete(self):
        logger.debug("Inside delete me")
        return self.response.getResponse(400, "Unimplemented exception")