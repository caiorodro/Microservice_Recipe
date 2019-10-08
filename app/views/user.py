import json
from flask import jsonify
import app.base.QModel as ctx 
from app.base.QBase import qBase
from app.base.mapTable import mapUser
from app.base.authentication import authentication
from werkzeug.security import generate_password_hash, check_password_hash
import unittest
from app.base.loggerNoSQL import loggerNoSQL, kindOfLog
import traceback

class user(unittest.TestCase):

    def __init__(self, keep=None, idUser=None):
        self.qBase = qBase(keep)
        self.__loggerNoSQL = loggerNoSQL()
        self.__listOfUsers = []
        self.__idUser = idUser
        self.__recUser = None

    def listUsers(self, name=None, email=None):
        btnEdit = '<button class="btn btn-primary waves-effect waves-light btn-sm m-b-5" onclick="edita({});" title="Editar"><i class="ti-pencil"></i></button>'
        btnDelete = '<button class="btn btn-danger waves-effect waves-light btn-sm m-b-5" onclick="deleta({});" title="Deletar"><i class="ti-trash"></i></button>'

        select1 = ctx.session.query(
            ctx.mapUser.ID_USER,
            ctx.mapUser.NAME_USER,
            ctx.mapUser.EMAIL,
            ctx.mapUser.USER_ENABLED,
            ctx.mapUser.KIND_OF_USER).order_by(ctx.mapUser.NAME_USER)

        if name is not None:
            select1 = select1.filter(ctx.mapUser.NAME_USER.like('%{}%'.format(name)))

        if email is not None:
            select1 = select1.filter(ctx.mapUser.EMAIL.like('%{}%'.format(email)))

        select1 = select1.all()

        [(self.__listOfUsers.append((row.ID_USER,
            row.NAME_USER,
            row.EMAIL,
            'Sim' if row.USER_ENABLED == 1 else 'Não',
            'Administrator' if row.KIND_OF_USER == 1 else 'User',
            btnEdit.format(str(row.ID_USER)), 
            btnDelete.format(str(row.ID_USER))))) for row in select1]

        return len(self.__listOfUsers)

    def saveUser(self, userMap=mapUser):

        try:
            pass1 = generate_password_hash(userMap.PASSWORD_USER)

            cmd = None

            if userMap.ID_USER > 0:

                cmd = ctx.usuario.update().values(
                    NOME_USUARIO = userMap.NAME_USER.upper(),
                    SENHA_USUARIO = pass1,
                    EMAIL_USUARIO = userMap.EMAIL.lower(),
                    TIPO_USUARIO = userMap.KIND_OF_USER,
                    USUARIO_ATIVO = userMap.USER_ENABLED).\
                        where(ctx.mapUser.ID_USER == userMap.ID_USER)

            elif userMap.ID_USER == 0:
                
                cmd = ctx.user.insert().values(
                    NOME_USUARIO = userMap.NAME_USER.upper(),
                    SENHA_USUARIO = pass1,
                    EMAIL_USUARIO = userMap.EMAIL.lower(),
                    TIPO_USUARIO = userMap.KIND_OF_USER,
                    USUARIO_ATIVO = userMap.USER_ENABLED)

            ctx.session.execute(cmd)
            ctx.session.commit()

            return True
        except Exception as ex:
            self.__loggerNoSQL.newLog(ex.args[0], kindOfLog.ERROR, traceback.format_exc(),
                -1 if self.__idUser is None else self.__idUser)

            return False

    def deleteUser(self, ID_USER):

        try:
            q = ctx.session.query(ctx.mapUser).filter(ctx.mapUser.ID_USER == ID_USER)

            if not ctx.session.query(q.exists()).scalar():
                raise Exception('User not found')

            del1 = ctx.usuario.delete().where(ctx.mapUser.ID_USER == ID_USER)

            ctx.session.execute(del1)
            ctx.session.commit()

            return True
        except Exception as ex:
            _message = ex.args[0]
            self.__loggerNoSQL.newLog(_message, kindOfLog.ERROR, traceback.format_exc(),
                self.__idUser)

            return False

    def getUser(self, ID_USER):
        select1 = ctx.session.query(
            ctx.mapUser.ID_USER,
            ctx.mapUser.NAME_USER,
            ctx.mapUser.PASSWORD1,
            ctx.mapUser.EMAIL,
            ctx.mapUser.USER_ENABLED,
            ctx.mapUser.KIND_OF_USER).filter(ctx.mapUser.ID_USER == ID_USER).all()

        self.__recUser = self.qBase.toDict(select1)

        for item in self.__recUser:
            item['USER_ENABLED'] = float(item['USER_ENABLED'])

        return True

    def authenticateUser(self, EMAIL, PASSWORD):
        try:
            q = ctx.session.query(
                ctx.mapUser.EMAIL,
                ctx.mapUser.PASSWORD1
                ).filter(ctx.mapUser.EMAIL == EMAIL)

            if not ctx.session.query(q.exists()).scalar():
                return -1

            resultCheck = {}

            for item in q.all():
                resultCheck = { "password": check_password_hash(item[1], PASSWORD), "idUsuario": item[0] }

            if not resultCheck['password']:
                return -2

            self.__keep = authentication.encode_auth_token(resultCheck['idUsuario']).decode()
            self.__idUser = resultCheck['idUsuario']

            return (self.__keep, self.__idUser)
        except Exception as ex:
            trace = traceback.format_exc()
            self.__loggerNoSQL.newLog(ex.args[0], kindOfLog.ERROR, trace, self.__idUser)
            return -3

    def testAuthenticate(self, EMAIL, PASSWORD):
        result = self.authenticateUser(EMAIL, PASSWORD)

        if result == -1:
            message = "User not found"
            return self.qBase.toJsonRoute(message, 500)

        elif result == -2:
            message = "Wrong password"
            return self.qBase.toJsonRoute(message, 500)

        elif result == -3:
            message = "Unknown error. See the logs"
            return self.qBase.toJsonRoute(message, 500)

        elif isinstance(result, tuple):
            message = "Successfull authenticate"
            return self.qBase.toJsonRoute([self.__keep, self.__idUser], 200)

    def testListOfUsers(self, name=None, email=None):
        try:
            self.assertGreater(self.listUsers(name, email), 0)
            return self.qBase.toJson(self.__listOfUsers)

        except AssertionError as ae:
            self.__loggerNoSQL.newLog(ae.args[0], kindOfLog.INFO, traceback.format_exc(),
                -1 if self.__idUser is None else self.__idUser)

            return self.qBase.toJson(self.__listOfUsers)

    def testSaveUser(self, userMap=mapUser):
        try:
            self.assertTrue(self.saveUser(userMap=mapUser))
            
            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError as ae:
            _message = ae.args[0]
            self.__loggerNoSQL.newLog(_message, kindOfLog.INFO, traceback.format_exc(),
                -1 if self.__idUser is None else self.__idUser)

            return self.qBase.toJsonRoute(_message, 500)

    def testDeleteUser(self, idUser):
        try:
            self.assertTrue(self.deleteUser(idUser))

            return self.qBase.toJsonRoute("Ok", 200)
        except AssertionError:
            _message = "There is a problem to delete this user. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def testGetUser(self, ID_USER):
        try:
            self.assertTrue(self.getUser(ID_USER))

            return self.qBase.toJsonRoute(str(self.__recUser), 200)
        except AssertionError:
            _message = "There is a problem to delete this user. Look at the logs"

            return self.qBase.toJsonRoute(_message, 500)

    def close(self):
        try:
            ctx.conn.close()
        except:
            pass

    def __del__(self):
        self.close()