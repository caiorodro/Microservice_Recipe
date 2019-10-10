import json
from flask import jsonify
import app.base.QModel as ctx 
from app.base.QBase import qBase
from app.base.mapTable import mapRecipe
from venv.config import Config
from app.views.responses import Responses
import requests
import unittest
from app.base.logger import logger
from app.base.loggerNoSQL import loggerNoSQL, kindOfLog
import traceback

class recipe(qBase, unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        super().__init__(keep)
        self.idInserted = 0
        
        self.__logger = logger()
        self.__loggerNoSQL = loggerNoSQL()
        self.__idUser = idUser
        self.__lista1 = []
        self.__recipe = None
        self.qBase = qBase()

    def listOfRecipes(self, title=None):
        btnEdit = '<button class="btn btn-primary waves-effect waves-light btn-sm m-b-5" onclick="getRecipe({});" title="Edit"><i class="ti-pencil"></i></button>'
        btnDelete = '<button class="btn btn-danger waves-effect waves-light btn-sm m-b-5" onclick="delete({});" title="Delete"><i class="ti-trash"></i></button>'

        select1 = ctx.session.query(
            ctx.mapRecipe.ID_RECIPE,
            ctx.mapRecipe.TITLE,
            ctx.mapRecipe.READY_IN_MIN,
            ctx.mapRecipe.SERVING,
            ctx.mapRecipe.MASK).order_by(ctx.mapRecipe.TITLE)

        if title is not None:
            select1 = select1.filter(ctx.mapRecipe.TITLE.like('%{}%'.format(title)))

        self.__lista1 = []

        [(self.__lista1.append((row.ID_RECIPE,
            row.TITLE,
            row.READY_IN_MIN,
            row.SERVING,
            row.MASK,
            btnEdit.format(str(row.ID_RECIPE)), 
            btnDelete.format(str(row.ID_RECIPE))))) for row in select1.all()]

        return len(self.__lista1)

    def saveImage(self, recipeMap=mapRecipe, content=bytes):
        """
        Save recipe image on table and returns Id of created record

        Parameters: recipeMap -> mapRecipe table. See the app.base.mapTable.py on mapRecipe class
        """

        cmd = ctx.recipe.insert()

        data1 = {
            'TITLE': recipeMap.TITLE,
            'INGREDIENTS': recipeMap.INGREDIENTS,
            'INSTRUCTIONS': recipeMap.INSTRUCTIONS,
            'IMAGE_NAME': recipeMap.IMAGE_NAME,
            'IMAGE': content,
            'MASK': recipeMap.MASK,
            'READY_IN_MIN': int(recipeMap.READY_IN_MIN),
            'SERVING': int(recipeMap.SERVING)
        }

        stm = ctx.session.execute(cmd, data1)

        self.__idInserted = list(stm.inserted_primary_key)[0]

        self.__logger.logInfo('New recipe ID: {} registered'.format(self.__idInserted))

        ctx.session.commit()

        return self.__idInserted

    def saveRecipe(self, recipeMap=mapRecipe):
        """
        Save recipe data after image was uploaded and saved in table
        You have to send data without IMAGE BLOB and ID_RECIPE filled on
        recipeMap parameter

        Parameters: recipeMap -> mapRecipe table. See the app.base.mapTable.py on mapRecipe class
        """

        query = ctx.session.query(
            ctx.mapRecipe.IMAGE_NAME,
            ctx.mapRecipe.IMAGE).filter(ctx.mapRecipe.ID_RECIPE == recipeMap.ID_RECIPE)

        list1 = list(query)

        imgName = list1[0].IMAGE_NAME
        img = list1[0].IMAGE

        cmd = ctx.recipe.update().values(
            TITLE = recipeMap.TITLE,
            INGREDIENTS = recipeMap.INGREDIENTS,
            INSTRUCTIONS = recipeMap.INSTRUCTIONS,
            MASK = recipeMap.MASK,
            READY_IN_MIN = recipeMap.READY_IN_MIN,
            SERVING = recipeMap.SERVING).where(ctx.mapRecipe.ID_RECIPE == recipeMap.ID_RECIPE)

        ctx.session.execute(cmd)

        try:
            payload = {
                'backgroundImage': imgName,
                'image': img,
                'ingredients': recipeMap.INGREDIENTS,
                'instructions': recipeMap.INSTRUCTIONS,
                'mask': recipeMap.MASK,
                'readyInMinutes': recipeMap.READY_IN_MIN,
                'servings': recipeMap.SERVING,
                'title': recipeMap.TITLE
            }

            # responseAPI = requests.request("POST", Config.URL_RAPID_API_MICROSERVICE, data=payload)

            # print(responseAPI.text)

            ctx.session.commit()

            return 'result'
        except Exception as ex:
            ctx.session.rollback()
            raise Exception(ex.args[0])

    def getRecipe(self, ID_RECIPE):

        self.__recipe = None

        def testIt():
            _table = ctx.mapRecipe

            select1 = ctx.session.query(
                _table.ID_RECIPE,
                _table.TITLE,
                _table.INGREDIENTS,
                _table.INSTRUCTIONS,
                _table.IMAGE_NAME,
                _table.MASK,
                _table.READY_IN_MIN,
                _table.SERVING).filter(_table.ID_RECIPE == ID_RECIPE).all()

            self.__recipe = self.qBase.toDict(select1)

            return self.__recipe

        try:
            self.assertIsInstance(testIt(), list)

            return self.qBase.toJsonRoute(str(self.__recipe), 200)
        except AssertionError as ae:
            error = 'Error on get recipe \n' + ae.args[0]
            return self.qBase.toJsonRoute(error, 500)

    def __sendDataToAPI(self, data):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/visualizeRecipe"

        recipeData = data

        payload = Responses.dictToStr(recipeData)

        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': "63facb4255mshb733c998f7d7f9bp128ac2jsn1587e6415a8b",
            'content-type': "multipart/form-data; boundary=---011000010111000001101001"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.text

    def testListOfRecipe(self, title=None):
        """
        Tests the list of recipe

        Return: returns the __lista1 list filled variable
        """
        try:
            self.assertGreater(self.listOfRecipes(title), 0)

            return super().toJson(self.__lista1)
        except AssertionError:
            _message = 'Error. Get list of {} recipe(s)'.format(str(len(self.__lista1)))

            self.__loggerNoSQL.newLog(_message, kindOfLog.ERROR, traceback.format_exc(), self.__idUser)

            return super().toJson(self.__lista1)

    def testSaveRecipe(self, recipeMap=mapRecipe, content=bytes):
        """
        Tests the save of recipe
        Parameters: 'recipeMap' object that contains fields of table tb_recipe and 
            'content' -> bytes of image recipe

        Return: returns number record inserted
        """

        try:
            self.assertGreater(self.saveImage(recipeMap, content), 0)

            return super().toJsonRoute(str(self.__idInserted), 200)
        except AssertionError:
            _message = 'Error. Get list of {} recipe(s)'.format(str(len(self.__lista1)))

            self.__loggerNoSQL.newLog(_message, kindOfLog.INFO, traceback.format_exc(), self.__idUser)

            return super().toJsonRoute(str(self.__idInserted), 200)
