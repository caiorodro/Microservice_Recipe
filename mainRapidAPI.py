from flask import Flask
from app.views.routeRapidAPI import dataRapidAPI
import os

cwd = os.getcwd()

templates = '/'.join((cwd, 'app/templates/'))
app = Flask(__name__, template_folder=templates, static_url_path="")

packs = [dataRapidAPI]

[app.register_blueprint(pack) for pack in packs]

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005, use_reloader=True)
