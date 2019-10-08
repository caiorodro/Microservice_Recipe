import os
from flask import Blueprint
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import url_for, jsonify
import json
from app.views.user import user
from app.base.mapTable import mapUser
from app.base.loggerNoSQL import loggerNoSQL

dataUser = Blueprint('dataUser', __name__)

@dataUser.route('/authenticateUser', methods=['POST'])
def authenticateUser():
    rec = json.loads(request.get_data())

    userx =  rec['EMAIL']
    password = rec['PASSWORD']
    idUser = rec['idUser']

    try:
        user1 = user(None, idUser)
        backData = user1.testAuthenticate(userx, password)
        del user1

        return backData
    except Exception as ex:
        return jsonify({ "message": ex.args[0] }), 500

@dataUser.route('/listUsers', methods=['POST'])
def listUsers():
    rec = json.loads(request.get_data())

    nome = rec['nome']
    email = rec['email']

    user1 = user(rec['keep'])

    result = user1.testListOfUsers(nome, email)

    del user1

    return result

@dataUser.route('/getUser', methods=['POST'])
def getUser():

    rec = json.loads(request.get_data())

    ID_USER = rec['ID_USER']
    keep = rec['keep']

    user1 = user(keep)
    result = user1.getUser(ID_USER)

    del user1

    return result

@dataUser.route('/saveUser', methods=['POST'])
def saveUser():
    rec = json.loads(request.get_data())

    ID_USER = rec['ID_USER']
    NAME_USER = rec['NAME_USER']
    EMAIL = rec['EMAIL']
    PASSWORD_USER = rec['PASSWORD_USER']
    KIND_OF_USER = rec['KIND_OF_USER']
    USER_ENABLED = rec['USER_ENABLED']
    keep = rec['keep']
    idUser = rec['idUser']

    table = mapUser(ID_USER, NAME_USER, PASSWORD_USER, EMAIL, USER_ENABLED, KIND_OF_USER)

    user1 = user(keep, idUser)
    retorno = user1.testSaveUser(table)

    del user1

    return retorno

@dataUser.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    rec = json.loads(request.get_data())

    ID_USER = rec['ID_USER']
    keep = rec['keep']

    user1 = user(keep)
    user1.deleteUser(ID_USER)

    del user1

    return "Ok"

@dataUser.route('/listOfLogs', methods=['POST'])
def listOfLogs():
    rec = json.loads(request.get_data())

    keep = rec['keep']
    idUser = int(rec['idUser'])
    data1 = rec['data']
    start = int(rec['start'])
    limit = int(rec['limit'])

    log = loggerNoSQL()

    result = log.testListLogs(data1, start, limit)

    return result