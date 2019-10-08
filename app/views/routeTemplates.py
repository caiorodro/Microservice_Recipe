import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for
from flask import jsonify
import json
from app.views.recipe import recipe
from app.base.mapTable import mapUser, mapRecipe

cwd = os.getcwd()

dataTemplate = Blueprint('dataTemplate', __name__)

@dataTemplate.route('/app/templates/scripts/<path:path>')
def send_scripts(path):
    return send_from_directory('app/templates/scripts', path)

@dataTemplate.route('/app/templates/css/<path:path>')
def send_css(path):
    return send_from_directory('app/templates/css', path)

@dataTemplate.route('/app/csv/<path:filename>', methods=['GET', 'POST'])
def downloadCSV(filename):
    uploads = '/'.join((cwd, 'app/csv/'))
    return send_from_directory(directory=uploads, filename=filename)

@dataTemplate.route('/app/templates/assets/<path:path>')
def send_assets(path):
    return send_from_directory('app/templates/assets', path)

@dataTemplate.route('/app/templates/assets/images/<path:path>')
def send_assets_images(path):
    return send_from_directory('app/templates/assets/images', path)

@dataTemplate.route('/app/templates/images/<path:path>')
def send_images(path):
    return send_from_directory('app/templates/images', path)

@dataTemplate.route('/app/templates/dist/<path:path>')
def send_dist(path):
    return send_from_directory('app/templates/dist', path)

@dataTemplate.route("/")
def hello():
    return render_template('painel1.html')

@dataTemplate.route('/doUpload', methods=['POST'])
def doUpload():
    file = None

    for item in request.files:
        file = request.files[item]

    jsonData = json.loads(request.form['jsonData'])

    content = file.read()

    data = mapRecipe(0, jsonData['TITLE'], 
        jsonData['INGREDIENTS'], 
        jsonData['INSTRUCTIONS'], 
        file.name, 
        '', 
        jsonData['MASK'], 
        int(jsonData['READY_IN_MINUTES']), 
        int(jsonData['SERVING']))

    try:
        dataImage = recipe(jsonData['keep'])
        retorno = dataImage.testSaveRecipe(data, content)
        del dataImage

        return retorno
    except Exception as ex:
        return jsonify({ "message": ex.args[0] }), 500

@dataTemplate.route('/saveRecipe', methods=['POST'])
def saveRecipe():

    jsonData = json.loads(request.get_data())

    data = mapRecipe(int(jsonData['ID_RECIPE']),
        jsonData['TITLE'],
        jsonData['INGREDIENTS'],
        jsonData['INSTRUCTIONS'],
        '',
        None,
        jsonData['MASK'],
        int(jsonData['READY_IN_MIN']),
        int(jsonData['SERVING']))

    data1 = recipe(jsonData['keep'])
    retorno = data1.saveRecipe(data)
    del data1

    return retorno

@dataTemplate.route('/listOfRecipes', methods=['POST'])
def listOfRecipes():
    jsonData = json.loads(request.get_data())

    title = jsonData['TITLE']
    keep = jsonData['keep']
    idUser = jsonData['idUser']

    data1 = recipe(keep, idUser)
    retorno = data1.testListOfRecipe(title)
    del data1

    return retorno