class mapUser(object):
    def __init__(self, ID_USER, NAME_USER, PASSWORD1, EMAIL, USER_ENABLED, KIND_OF_USER):
        self.ID_USER = ID_USER
        self.NAME_USER = NAME_USER
        self.PASSWORD1 = PASSWORD1
        self.EMAIL = EMAIL
        self.USER_ENABLED = USER_ENABLED
        self.KIND_OF_USER = KIND_OF_USER

class mapRecipe(object):
    def __init__(self, ID_RECIPE, TITLE, INGREDIENTS, INSTRUCTIONS, IMAGE_NAME, IMAGE, MASK, READY_IN_MIN, SERVING):
        self.ID_RECIPE = ID_RECIPE
        self.TITLE = TITLE
        self.INGREDIENTS = INGREDIENTS
        self.INSTRUCTIONS = INSTRUCTIONS
        self.IMAGE_NAME = IMAGE_NAME
        self.IMAGE = IMAGE
        self.MASK = MASK
        self.READY_IN_MIN = READY_IN_MIN
        self.SERVING = SERVING
        
