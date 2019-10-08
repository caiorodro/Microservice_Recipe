from flask import Flask

flaksApp = Flask(__name__)

if __name__ == '__main__':
    from logger import *
    flaksApp.run(host='127.0.0.1', port=5014, debug=False, use_reloader=True)
