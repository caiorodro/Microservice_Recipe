
class Responses:

    responses = [{
        "code": 200,
        "description": "Ok"
    }, {
        "code": 201,
        "description": "Created"
    }, {
        "code": 400,
        "description": "Bad request"
    }, {
        "code": 401,
        "description": "Unauthorized"
    }, {
        "code": 404,
        "description": "Not found"
    }, {
        "code": 405,
        "description": "Method not allowed"
    }, {
        "code": 409,
        "description": "Conflict [POST, GET, PUT or DELETE]"
    }, {
        "code": 500,
        "description": "Internal server error"
    }]

    def getResponse(self, statusCode, result):
        found = list(filter(lambda item: item['code'] == statusCode, self.responses))

        message = found[0]['description'] if len(found) > 0 else "Status code not found"

        return { "message": message, "result": result }, statusCode

    @staticmethod
    def dictToStr(dict1):
        
        str1 = []

        for key, value in dict1.items():
            val = str(value)
            str1.append(''.join((key, '=', val,)))

        return '&'.join(str1)
