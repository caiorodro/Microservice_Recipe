import jwt
from datetime import datetime, timedelta
from venv.config import Config
import os
import pytest
import unittest

class authentication(unittest.TestCase):
    def __init__(self):
        pass

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=0),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            raise e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY, algorithm='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise Exception('Token expirado. Faça o login novamente')
        except jwt.InvalidTokenError:
            raise Exception('Token inválido. Faça o login novamente')