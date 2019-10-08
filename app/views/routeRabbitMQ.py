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
from app.base.rabbit import workerMQ
from app.base.QBase import qBase

dataRabbitMQ = Blueprint('dataRabbitMQ', __name__)

@dataRabbitMQ.route('/startWorker', methods=['GET'])
def startWorker():

    #rec = json.loads(request.get_data())

    #idUser = int(rec['idUser'])
    idUser = 1

    with workerMQ(idUser) as wk:
        print(type(wk))
        wk.testRunWorker()

    return qBase.toJsonRoute("RabbitMQ worker started", 200)
