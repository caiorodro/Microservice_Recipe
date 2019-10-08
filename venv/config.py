class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xe58\xcf\x95\x91q\xde\xbf\x96lD\x1eA\x0fkC\xcaO\x10\xd6\x1a8\xf1\xfc"

    DB_SERVER_NAME = "localhost:3306"
    DB_NAME = "Recipe"
    DB_USERNAME = "root"
    DB_PASSWORD = "xyz"

    ZIP_UPLOADS = "/Users/caioDoran/Documents/Projects/DataDev/csv"
    ZIP_DOWNLOADS = '/Users/caioDoran/Documents/Projects/DataDev/csv'
    ZIP_ADDRESS = 'http://127.0.0.1:5000/csv/'

    URL_RAPID_API_MICROSERVICE = "http://127.0.0.1:5005/api/v1.0/taskManageRecipe"

    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xe58\xcf\x95\x91q\xde\xbf\x96lD\x1eA\x0fkC\xcaO\x10\xd6\x1a8\xf1\xfc"

    DB_SERVER_NAME = "localhost:3306"
    DB_NAME = "Recipe"
    DB_USERNAME = "root"
    DB_PASSWORD = "yyz"

    ZIP_UPLOADS = "/Users/caioDoran/Documents/Github/DataDev/csv"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_SERVER_NAME = "localhost:3306"
    DB_NAME = "Recipe"
    DB_USERNAME = "root"
    DB_PASSWORD = "yyz"

    SESSION_COOKIE_SECURE = False