import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for
import json
import requests
from venv.config import Config

dataRapidAPI = Blueprint('dataRapidAPI', __name__)

@dataRapidAPI.route('/saveRecipe', methods=['POST'])
def saveRecipe():
    jsonData = json.loads(request.get_data())

    payload = {
        'backgroundImage': jsonData['backgroundImage'],
        'image': b'x',
        'ingredients': jsonData['ingredients'],
        'instructions': jsonData['instructions'],
        'mask': jsonData['mask'],
        'readyInMinutes': int(jsonData['readyInMinutes']),
        'servings': int(jsonData['servings']),
        'title': jsonData['title']
    }

    response = requests.request("POST", Config.URL_RAPID_API_MICROSERVICE, data=payload)

    return response.getResponse(200, response.text)
