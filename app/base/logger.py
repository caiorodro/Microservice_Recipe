import logging
# import logging.config

class logger:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.handler = logging.FileHandler('recipe.log')
        self.handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)

        self.logger.addHandler(self.handler)

    def __flushHandle(self):
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(self.handler)

    def logInfo(self, message):
        self.__flushHandle()
        self.logger.info(message)

    def logError(self, message):
        self.__flushHandle()
        self.logger.error(message)
